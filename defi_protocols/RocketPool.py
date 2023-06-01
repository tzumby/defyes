import logging
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_node
from defi_protocols.eth_derivs import EthDerivative
from web3 import Web3

logger = logging.getLogger(__name__)

ROCKET_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'

Rocket = EthDerivative(
    protocol="Rocket Pool",
    description="Rocket Pool ETH",
    blockchain=ETHEREUM,
    addr=ROCKET_ADDR,
    underlying_token='0x0000000000000000000000000000000000000000',
    eth_value_function='getEthValue',
    eth_value_abi='[{"inputs":[{"internalType":"uint256","name":"_rethAmount","type":"uint256"}],"name":"getEthValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
)


def underlying(wallet: str, block: int | str, blockchain: str, decimals: bool = True, web3: Web3 = None, unwrapped: bool=True) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)
    value = Rocket.underlying(wallet=wallet, block=block, decimals=decimals, web3=web3, unwrapped=unwrapped)
    if unwrapped:
        return [[Rocket.underlying_token, value]]
    else:
        return [[Rocket.addr, value]]
