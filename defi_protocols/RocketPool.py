import logging
from defi_protocols.functions import get_node
from defi_protocols.util.EthDerivs import EthDerivative
from web3 import Web3

logger = logging.getLogger(__name__)

ROCKET_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'

def underlying(wallet: str, block: int | str, blockchain: str, decimals: bool=True, web3: Web3=None)->list:
    deriv_address = ROCKET_ADDR
    if web3 is None:
        web3 = get_node(blockchain, block=block)
    deriv_object = EthDerivative(deriv_address, web3=web3, decimals=decimals)
    return [[deriv_object.underlying_token, deriv_object.underlying(wallet, block)]]

