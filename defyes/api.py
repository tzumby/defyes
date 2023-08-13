import time

import requests
from web3 import Web3

from defyes.cache import cache_call
from defyes.constants import EXPLORERS, TESTNET_CHAINS, Chain
from defyes.node import get_node

TESTNET_HEADER = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
}


class ChainExplorer(requests.Session):
    def __init__(self, blockchain: str = None) -> None:
        super().__init__()
        self.chain = blockchain
        if blockchain in TESTNET_CHAINS:
            self.headers.update(TESTNET_HEADER)
        domain, apikey = EXPLORERS[blockchain]
        self.params["apikey"] = apikey
        self.url = f"https://{domain}/api"

    def _get(self, **params):
        response = self.request("GET", self.url, params=params)
        response.raise_for_status()
        return response

    cached = cache_call(
        exclude_args=["self"],
        filter=lambda args: "latest" not in args,
        include_attrs=[
            lambda self: self.__class__.__name__,
            lambda self: self.chain,
        ],
    )

    @cached
    def block_from_time(self, timestamp: int) -> int:
        response = self._get(module="block", action="getblocknobytime", closest="before", timestamp=int(timestamp))
        block_id = response.json()["result"]
        try:
            return int(block_id)
        except (TypeError, ValueError):
            return block_id

    @cached
    def time_from_block(self, block: int | str) -> int:
        if isinstance(block, str):
            if block == "latest":
                return int(time.time())

        response = self._get(module="block", action="getblockreward", blockno=block)
        timestamp = response.json()["result"]["timeStamp"]
        try:
            return int(timestamp)
        except (TypeError, ValueError):
            return timestamp


def latest_not_in_params(args):
    return "latest" not in args


class Explorer:
    TESTNET_HEADER = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
    }
    blockchain = None
    query = None

    def __init__(self, blockchain: str = None) -> None:
        if self.blockchain is None:
            self.blockchain = blockchain
        self.url = EXPLORERS[self.blockchain][0]
        self.key = EXPLORERS[self.blockchain][1]

        self.query = self.query.format(url=self.url, key=self.key)


class ABIError(Exception):
    pass


class GetABI(Explorer):
    query = "https://{url}/api?module=contract&action=getabi&address=%s&apikey={key}"

    @cache_call(is_method=True)
    def make_request(self, contract_address: str):
        result = None
        contract_address = get_implemented_contract(self.blockchain, contract_address)
        result = requests.get(self.query % contract_address).json()["result"]
        if result == "Contract source code not verified":
            raise ABIError("ABI not verified.")
        return result


class GetContractCreation(Explorer):
    blockchain = Chain.ETHEREUM
    query = "https://{url}/api?module=contract&action=getcontractcreation&contractaddresses=%s&apikey={key}"

    @cache_call(filter=latest_not_in_params, is_method=True)
    def make_request(self, contract_address: str):
        contract_address = get_implemented_contract(self.blockchain, contract_address)
        return requests.get(self.query % contract_address).json()["result"]


class GetLogs(Explorer):
    KEYS_WHITELIST = [
        "topic1",
        "topic2",
        "topic3",
        "topic0_1_opr",
        "topic0_2_opr",
        "topic0_3_opr",
        "topic1_2_opr",
        "topic1_3_opr" "topic2_3_opr",
    ]
    query = "https://{url}/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey={key}"

    @cache_call(is_method=True)
    def make_request(
        self, contract_address: str, from_block: int, to_block: int, topic0: str, optional_params: dict = {}
    ):
        contract_address = get_implemented_contract(self.blockchain, contract_address)
        params = ""
        for key, value in optional_params.items():
            if key in self.KEYS_WHITELIST and value:
                params += f"&{key}={value}"
        self.query += params
        return requests.get(self.query % (from_block, to_block, contract_address, topic0)).json()["result"]


class TXList(Explorer):
    query = "https://{url}/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey={key}"

    @cache_call(is_method=True)
    def make_request(self, contract_address: str, block_start: int, block_end: int):
        return requests.get(self.query % (contract_address, block_start, block_end)).json()["result"]


def get_implemented_contract(blockchain, proxy_address):
    proxy_address = Web3.to_checksum_address(proxy_address)
    node = get_node(blockchain)
    bytecode = node.eth.get_code(proxy_address).hex()

    # Check for EIP-1167 proxy implementation
    if bytecode[2:22] == "363d3d373d3d3d363d73" and bytecode[62:] == "5af43d82803e903d91602b57fd5bf3":
        return "0x" + bytecode[22:62]
    hash_value = Web3.keccak(text="eip1967.proxy.implementation")
    impl_slot = (int.from_bytes(hash_value, byteorder="big") - 1).to_bytes(32, byteorder="big")
    impl_contract = (
        "0x"
        + Web3.to_hex(
            node.eth.get_storage_at(
                proxy_address,
                impl_slot.hex(),
            )
        )[-40:]
    )
    impl_function = Web3.keccak(text="implementation()")[:4].hex()[2:]

    # FIXME: this is not a correct way to identify EIP-1967 proxy contracts
    if len(bytecode) >= 1000:
        return proxy_address
    elif len(bytecode) < 150:
        return "0x" + bytecode[32:72]
    elif impl_function in bytecode:
        contract_abi = '[{"constant":true,"inputs":[],"name":"implementation","outputs":[{"name":"impl","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
        contract_instance = node.eth.contract(proxy_address, abi=contract_abi)
        impl_call = contract_instance.functions.implementation().call()
        return impl_call
    elif impl_contract == "0x0000000000000000000000000000000000000000":
        safe_impl_contract = "0x" + Web3.to_hex(node.eth.get_storage_at(proxy_address, 0))[-40:]
        return safe_impl_contract
    else:
        return impl_contract


class GetTokenTX(Explorer):
    query = "https://{url}/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey={key}"

    @cache_call(filter=latest_not_in_params, is_method=True)
    def make_request(self, token_address: str, contract_address: str, block_start: str, block_end: str):
        return requests.get(self.query % (contract_address, token_address, block_start, block_end)).json()["result"]


class GetEtherscanPrice(Explorer):
    blockchain = Chain.ETHEREUM
    query = "https://{url}/api?module=token&action=tokeninfo&contractaddress=%s&apikey={key}"

    def make_request(self, token_address: str):
        price = requests.get(self.query % token_address).json()["result"][0]["tokenPriceUSD"]
        return price, "etherscan", Chain.ETHEREUM
