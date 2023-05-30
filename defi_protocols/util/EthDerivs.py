import logging
from dataclasses import dataclass, field
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, balance_of, get_contract, to_token_amount

logger = logging.getLogger(__name__)

DERIVS_DB = {
    '0xae78736Cd615f374D3085123A210448E74Fc6393': {
        'protocol': "Rocket Pool",
        'name': "Rocket Pool ETH",
        'blockchain': 'ethereum',
        'underlying': '0x0000000000000000000000000000000000000000',
        'eth_value_function': 'getEthValue',
        'eth_value_abi': '[{"inputs":[{"internalType":"uint256","name":"_rethAmount","type":"uint256"}],"name":"getEthValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    },
    '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb': {
        'protocol': "Ankr",
        'name': "Ankr Staked ETH",
        'blockchain': 'ethereum',
        'underlying': '0x0000000000000000000000000000000000000000',
        'eth_value_function': 'sharesToBonds',
        'eth_value_abi': '[{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sharesToBonds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    },
}


@dataclass
class EthDerivative:
    protocol: str = field(init=False)
    addr: str
    web3: Web3 = None
    decimals: bool = True
    blockchain: str = field(init=False)
    underlying_token: str = field(init=False)
    eth_value_function: str = field(init=False)
    eth_value_abi: str = field(init=False)

    def __post_init__(self):
        self.blockchain = DERIVS_DB[self.addr]['blockchain']
        if self.web3 is None:
            self.web3 = get_node(self.blockchain, block='latest')
        self.protocol = DERIVS_DB[self.addr]['protocol']
        self.addr = self.web3.to_checksum_address(self.addr)
        self.eth_value_abi = DERIVS_DB[self.addr]['eth_value_abi']
        self.contract_instance = get_contract(self.addr, self.blockchain, abi=self.eth_value_abi)
        self.eth_value_function = DERIVS_DB[self.addr]['eth_value_function']
        self.name = DERIVS_DB[self.addr]['name']
        self.underlying_token = DERIVS_DB[self.addr]['underlying']

    def underlying(self, wallet: str, block: int | str)->Decimal:
        wallet = self.web3.to_checksum_address(wallet)
        amount = balance_of(wallet, self.addr, block, self.blockchain, decimals=False)
        eth_value = self.contract_instance.functions[self.eth_value_function](int(amount)).call(block_identifier=block)
        return to_token_amount(self.underlying_token, amount=eth_value, blockchain=self.blockchain, web3=self.web3, decimals=self.decimals)