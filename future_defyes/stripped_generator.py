from pathlib import Path


def get_module_path(module_file):
    return Path(module_file).resolve().parent


def load_abi(module_file_path, abi_filename):
    protocol_path = get_module_path(module_file_path)
    path = protocol_path / "abis" / abi_filename
    with open(path) as f:
        return f.read()
