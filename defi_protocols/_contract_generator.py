import re

def camel_to_snake(camel_case):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def generate_methods_from_abi(abi_string, const_call_methods=[]):
    TYPE_CONVERSION = {
            'uint64': 'int',
            'uint256': 'int',
            'address': 'str'
            }

    abi_list = eval(abi_string)

    methods = []
    for item in abi_list:
        method_name = item['name']
        method_name_snake = camel_to_snake(method_name)
        method_str = ""

        args = []
        args_names = []
        for arg in item['inputs']:
            arg_name = arg.get('name', '')
            if arg_name:
                arg_name = camel_to_snake(arg_name)
            else:
                arg_name = 'RENAME'
            args_names.append(arg_name)

            try:
                arg_type = TYPE_CONVERSION[arg['type']]
            except KeyError:
                arg_type = arg['type']

            args.append(f'{arg_name}: {arg_type}')

        if args:
            args_str = ', ' + ', '.join(args)
            args_names = ', '.join(args_names)
        else:
            method_str += "    @property\n"
            args_str = ''
            args_names = ''

        outputs = item.get('outputs', [])
        if outputs:
            return_str = ''
            return_comment = ''
            return_types = []
            return_names = []
            for output in outputs:
                output_type = output.get('type', '')
                output_name = output.get('name', '')
                try:
                    return_type = TYPE_CONVERSION[output_type]
                except KeyError:
                    return_type = output_type
                return_types.append(return_type)
                return_names.append(output_name)

            if len(return_types) == 1:
                return_str = f' -> {return_types[0]}'
            else:
                return_str = f' -> Tuple[{", ".join(return_types)}]'
                return_comment = f'        # Output: {", ".join(return_names)}\n'


        if method_name in const_call_methods:
            ret = f"        return const_call(self.contract.functions.{method_name}({args_names}))\n"
        else:
            ret = f"        return self.contract.functions.{method_name}({args_names}).call(block_identifier=self.block)\n"
        method_str += f"    def {method_name_snake}(self{args_str}){return_str}:\n"
        method_str += return_comment if return_comment else ''
        method_str += ret

        methods.append(method_str)

    return '\n'.join(methods)


contract_class_template = """
class {}:
    ABI: str = {}\n
    BLOCKCHAIN: str
    ADDR: str

    def __init__(self, block) -> None:
        node = get_node(self.BLOCKCHAIN, block)
        self.contract = node.eth.contract(address=self.ADDR, abi=self.ABI)\n
"""

def generate_contract_class(class_name, abi_string, const_call_methods=[]):
    result = contract_class_template.format(class_name, abi_string)
    result += generate_methods_from_abi(abi_string, const_call_methods)

    return result

