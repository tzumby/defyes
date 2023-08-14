from typing import Union

from web3 import Web3

from defyes.api import ChainExplorer
from defyes.node import get_node


def get_safe_functions(tx_hash: str, block: Union[int, str], blockchain: str, web3=None) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    tx_receipt = web3.eth.get_transaction(tx_hash)
    tx_to = tx_receipt["to"]
    tx_input_data = tx_receipt["input"]

    tx_to_impl_code = bytes.fromhex(Web3.to_hex(web3.eth.get_storage_at(tx_to, 0))[2:])
    proxy_address = Web3.to_checksum_address(tx_to_impl_code[-20:].hex())
    proxy_address_abi = ChainExplorer(blockchain).abi_from_address(proxy_address)
    proxy_contract = web3.eth.contract(address=proxy_address, abi=proxy_address_abi)

    input_data = proxy_contract.decode_function_input(tx_input_data)
    functions, params = input_data
    if "execTransaction" in str(functions):
        input_data = proxy_contract.decode_function_input(tx_input_data)
        input_data_contract_address = params["to"]
        input_data_abi = ChainExplorer(blockchain).abi_from_address(input_data_contract_address)

        input_data_contract = web3.eth.contract(address=input_data_contract_address, abi=input_data_abi)
        input_data_bytes = input_data_contract.decode_function_input(params["data"].hex())
        functions2, params2 = input_data_bytes
        if "multiSend" in str(functions2):
            transaction = params2["transactions"].hex()
            function_list = decode_multisend_transaction(transaction, web3, blockchain)
            return function_list
        elif "execTransactionWithRole" in str(functions2):
            data_output = decode_function_input(params2["to"], params2["data"], blockchain, web3)
            decode_dict = {
                "operation": params2["operation"],
                "to_address": params2["to"],
                "value": params2["value"],
                "role": params2["role"],
                "data_output": data_output,
            }
            return decode_dict
        else:
            decode_dict = {
                "operation": params["operation"],
                "to_address": params["to"],
                "value": params["value"],
                "data_output": input_data_bytes,
            }
            return decode_dict
    else:
        print("not a safe transaction")


def decode_multisend_transaction(input_data: str, web3, blockchain: str) -> list:
    function_list = []
    for i in range(0, 10):
        operation = input_data[:2]
        to_address = "0x" + input_data[2:42]
        value = input_data[42:106]
        data_length = int("0x" + input_data[106:170].lstrip("0"), 16)
        data_rest = input_data[170 : 170 + (data_length * 2)]
        data_output = decode_function_input(to_address, data_rest, blockchain, web3)
        decode_dict = {
            "operation": operation,
            "to_address": to_address,
            "value": value,
            "data_length": data_length,
            "data_output": data_output,
        }
        function_list.append(decode_dict)
        input_data = input_data[170 + (data_length * 2) :]
        if len(input_data) == 0:
            break
    return function_list


def decode_function_input(function_address: str, input_hex: str, blockchain: str, web3) -> tuple:
    if function_address[:2] == "0x":
        checksum_address = Web3.to_checksum_address(function_address)
    else:
        checksum_address = Web3.to_checksum_address("0x" + function_address)
    function_abi = ChainExplorer(blockchain).abi_from_address(checksum_address)
    function_contract = web3.eth.contract(address=checksum_address, abi=function_abi)
    function_decode = function_contract.decode_function_input(input_hex)
    return function_decode
