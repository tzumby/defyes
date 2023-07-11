from web3 import Web3
from web3.types import HexBytes


def topic_creator(function: str) -> str:
    chunks = function.split(" ")
    types = ["bytes32", "uint256", "address", "uint48"]
    type_list = [chunk for chunk in chunks if chunk in types]

    return Web3.keccak(text="{}({})".format(chunks[0], ",".join(map(str, type_list)))).hex()


def address_hexor(address: str) -> str:
    return str("{}000000000000000000000000{}".format(address[:2], address[2:]))


def encode_address_hexor(address: str):
    return "0x000000000000000000000000" + address[2:]


def decode_address_hexor(address: HexBytes):
    return address.hex().replace("0x000000000000000000000000", "0x")
