import importlib.resources as pkg_resources
import itertools
import json
import keyword
import re
import textwrap
from pathlib import Path


def get_module_path(module_file):
    return Path(module_file).resolve().parent


current_module_path = get_module_path(__file__)


def get_defabipedia_path(protocol):
    try:
        with pkg_resources.path(f"defabipedia.{protocol}", "") as dir_path:
            if dir_path.exists() and dir_path.is_dir():
                return dir_path
    except (ModuleNotFoundError, FileNotFoundError):
        pass
    return None


def load_abi(module_file_path, abi_filename):
    protocol_path = get_module_path(module_file_path)
    defabipedia_path = get_defabipedia_path(protocol_path.name)

    path = protocol_path / "abis" / abi_filename
    if not path.exists():
        path = defabipedia_path / abi_filename if defabipedia_path else None
    if path is None:
        raise FileNotFoundError

    with open(path) as f:
        return f.read()


def snake_to_camel(snake_case):
    words = snake_case.split("_")
    camel_case = "".join(word.title() for word in words)
    return camel_case


def camel_to_snake(camel_case):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_case)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def args_name_gen(used_names: set, start: int = 0):
    used_names_ = set(used_names)
    for index in itertools.count(start=start):
        name = f"arg{index}"
        while name in used_names_:
            name += "_"
        yield name
        used_names_.add(name)


def generate_methods_from_abi(abi_path, const_call_methods=[], always_include_methods=[]):
    TYPE_CONVERSION = {
        "uint8": "int",
        "uint64": "int",
        "uint16": "int",
        "uint32": "int",
        "uint96": "int",
        "uint256": "int",
        "int256": "int",
        "uint128": "int",
        "uint208": "int",
        "uint40": "int",
        "uint64[]": "list[int]",
        "uint256[]": "list[int]",
        "int256[]": "list[int]",
        "address": "str",
        "address[]": "list[str]",
        "string": "str",
        "bytes32": "bytes",
        "bytes32[]": "list[bytes]",
        "bytes4": "bytes",
        "tuple[]": "list[tuple]",
    }

    with open(abi_path) as f:
        abi_list = json.load(f)

    all_method_names = []
    methods = []
    for item in abi_list:
        if item["type"] in ["constructor", "receive", "error", "event"]:
            continue
        try:
            method_name = item["name"]
        except KeyError as e:
            raise KeyError(f"{e!r} for {item}") from e

        method_name_snake = camel_to_snake(method_name)
        if method_name_snake not in always_include_methods:
            item_state = item.get("stateMutability", "")
            if item_state == "nonpayable":
                continue
        if method_name_snake == "class":
            continue
        if method_name_snake == "list":
            method_name_snake = "_list"

        n = 1
        while method_name_snake in all_method_names:
            method_name_snake = method_name_snake + f"_{n}"
            n += 1
        all_method_names.append(method_name_snake)

        awesome_names = args_name_gen(used_names=set(arg.get("name", "") for arg in item["inputs"]))
        args = []
        args_names = []
        for arg, auto_name in zip(item["inputs"], awesome_names):
            arg_name = camel_to_snake(arg.get("name") or auto_name)
            if keyword.iskeyword(arg_name):
                arg_name += "_"
            arg_type = TYPE_CONVERSION.get(arg["type"], arg["type"])
            args.append(f"{arg_name}: {arg_type}")
            args_names.append(arg_name)

        method_str = ""
        if args:
            args_str = ", " + ", ".join(args)
            args_names = ", ".join(args_names)
        else:
            method_str += "    @property\n"
            args_str = ""
            args_names = ""

        return_str = ""
        return_docstring = ""
        outputs = item.get("outputs", [])
        if outputs:
            return_types = []
            return_names = []
            for output in outputs:
                output_type = output.get("type", "")
                output_name = output.get("name", "")
                try:
                    return_type = TYPE_CONVERSION[output_type]
                except KeyError:
                    return_type = output_type
                return_types.append(return_type)
                return_names.append(output_name)

            if len(return_types) == 1:
                return_str = f" -> {return_types[0]}"
            else:
                return_str = f' -> tuple[{", ".join(return_types)}]'
                return_docstring = f'        Output: {", ".join(return_names)}\n'
                lines = textwrap.wrap(return_docstring)
                return_docstring = "\n            ".join(lines)

        if method_name in const_call_methods:
            ret = f"        return const_call(self.contract.functions.{method_name}({args_names}))\n"
        else:
            ret = f"        return self.contract.functions.{method_name}({args_names}).call(block_identifier=self.block)\n"
        method_str += f"    def {method_name_snake}(self{args_str}){return_str}:\n"
        method_str += f'        """\n{return_docstring}\n        """\n' if return_docstring else ""
        method_str += ret

        methods.append(method_str)

    return "\n".join(methods)


header_template = """
'''
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import %(classes)s

# Optionally
class %(first_class)s(%(first_class)s):
    ...
'''
from web3 import Web3

from defyes.generator import load_abi
from karpatkit.node import get_node
"""

contract_class_template = """

class %(name)s:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError(
                    "No default_addresses defined when trying to guess the address."
                ) from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, %(abi)r))\n
"""


def generate_contract_class(class_name, abi_path, const_call_methods=[], always_include_methods=[]):
    abi_filename = abi_path.name
    result = contract_class_template % dict(name=class_name, abi=abi_filename)
    result += generate_methods_from_abi(abi_path, const_call_methods, always_include_methods)
    return result


def generate_classes():
    import black  # Because it's used just during development
    import isort  # Because it's used just during development

    setup_paths = current_module_path.glob("**/autogen_config.json")
    black_config = get_black_config()

    for setup_path in setup_paths:
        is_const_call_used = False

        protocol_path = setup_path.parent
        autogenerated_module_path = protocol_path / "autogenerated.py"
        defabipedia_path = get_defabipedia_path(protocol_path.name)

        with open(setup_path) as f:
            abis_to_process = json.load(f)

        content = ""
        classes_name = []
        for abi_name, config in abis_to_process.items():
            abi_path = protocol_path / "abis" / f"{abi_name}.json"
            if not abi_path.exists():
                abi_path = defabipedia_path / f"{abi_name}.json" if defabipedia_path else None
            class_name = snake_to_camel(abi_name)
            classes_name.append(class_name)
            const_call_methods = config.get("const_call", [])
            always_include_methods = config.get("always_include", [])
            if const_call_methods:
                is_const_call_used = True
            content += generate_contract_class(class_name, abi_path, const_call_methods, always_include_methods)

        if not content:
            continue

        final_header_template = header_template
        if is_const_call_used:
            final_header_template += "from karpatkit.cache import const_call\n"

        content = final_header_template % dict(classes=", ".join(classes_name), first_class=classes_name[0]) + content
        content = isort.code(content)
        content = black.format_file_contents(content, fast=True, mode=black_config)
        with open(autogenerated_module_path, "w") as f:
            f.write(content)
        relative_module_path = autogenerated_module_path.relative_to(Path().resolve())
        print(f"{relative_module_path} was created/updated.")


def get_black_config():
    import black  # Because it's used just during development

    pyproject_toml = black.find_pyproject_toml(".")
    conf_dict = black.parse_pyproject_toml(pyproject_toml)
    target_versions_strings = conf_dict.pop("target_version", ["py310"])
    target_versions = set(
        next(t for t in black.TargetVersion if t.name.lower() == target_version_str)
        for target_version_str in target_versions_strings
    )
    return black.Mode(target_versions=target_versions, **conf_dict)


if __name__ == "__main__":
    generate_classes()
