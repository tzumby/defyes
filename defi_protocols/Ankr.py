import logging

from web3 import Web3

from defi_protocols.eth_derivs import EthDerivative
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_node

logger = logging.getLogger(__name__)

ANKR_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'

Ankr = EthDerivative(
    protocol="Ankr",
    description="Ankr Staked ETH",
    blockchain=ETHEREUM,
    addr=ANKR_ADDR,
    underlying_token='0x0000000000000000000000000000000000000000',
    eth_value_function='sharesToBonds',
    eth_value_abi='[{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sharesToBonds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
)


def underlying(wallet: str, block: int | str, blockchain: str, decimals: bool = True, web3: Web3 = None) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)
    value = Ankr.underlying(wallet=wallet, block=block, decimals=decimals, web3=web3)
    return [[Ankr.underlying_token, value]]
