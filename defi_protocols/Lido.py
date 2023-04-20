from defi_protocols.functions import get_node, get_contract
from defi_protocols.constants import ETHEREUM, ZERO_ADDRESS
from typing import Union
from decimal import Decimal


STETH_ADDRESS = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
WSTETH_ADDRESS = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
STETH_PROXY_ABI = "0x47EbaB13B806773ec2A2d16873e2dF770D130b50"
STETH_DECIMALS = 18
WSTETH_DECIMALS = 18

STETH_ABI = '[{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
WSTETH_ABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stEthPerToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def underlying(wallet: str, block: Union[int, str], steth: bool = False, decimals: bool = True, web3: object = None) -> list:
    """
    Returns the balance of underlying ETH (or stETH if steth=True) corresponding to the stETH and wstETH held by a wallet.
    Parameters
    ----------
    wallet : str
        address of the wallet holding the position
    block : int or 'latest'
        block number at which the data is queried
    steth : bool
        if True the address of the underlying token returned is the Zero address, if False it is the stETH's address
    web3: obj
        optional, already instantiated web3 object
    decimals: bool
        specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True

    Returns
    ----------
    list
        a list where each element is a list with two elements, the underlying token address and its corresponding amount
    """
    balances = []

    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    wallet = web3.to_checksum_address(wallet)

    steth_contract = get_contract(STETH_ADDRESS, ETHEREUM, abi=STETH_ABI, block=block, web3=web3)
    steth_balance = steth_contract.functions.balanceOf(wallet).call(block_identifier=block)

    wsteth_contract = get_contract(WSTETH_ADDRESS, ETHEREUM, abi=WSTETH_ABI, block=block, web3=web3)
    wsteth_balance = wsteth_contract.functions.balanceOf(wallet).call(block_identifier=block)
    stEthPerToken = Decimal(wsteth_contract.functions.stEthPerToken().call(block_identifier=block))/(Decimal(10**18))

    steth_equivalent = steth_balance + wsteth_balance * stEthPerToken

    if decimals:
        steth_equivalent = float(steth_equivalent/Decimal(10**STETH_DECIMALS))
    else:
        steth_equivalent = int(steth_equivalent)

    if steth is True:
        balances.append([STETH_ADDRESS, steth_equivalent])
    else:
        balances.append([ZERO_ADDRESS, steth_equivalent])
    return balances


def unwrap(amount: Union[int, float], block: Union[int, str], steth: bool = False, web3: object = None) -> list:
    """
    Returns the balance of the underlying ETH (or stETH if steth=True) corresponding to the inputted amount of wstETH.
    Parameters
    ----------
    amount : int or float
        amount of wstETH; should be inputted with the corresponding decimals if decimals=True or as an int if decimals=False
    block : int or 'latest'
        block number at which the data is queried
    steth : bool
        if True the address of the underlying token returned is the Zero address, if False it is the stETH's address
    web3: obj
        optional, already instantiated web3 object

    Returns
    ----------
    list
        a list where the first element is the underlying token address and the second one is the balance
    """
    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    wsteth_contract = get_contract(WSTETH_ADDRESS, ETHEREUM, block=block, web3=web3)
    wsteth_balance = Decimal(amount)
    stEthPerToken = Decimal(wsteth_contract.functions.stEthPerToken().call(block_identifier=block)) / (
        Decimal(10 ** 18))

    #FIXME: return Decimal type
    steth_equivalent = float(wsteth_balance * stEthPerToken)

    if steth is True:
        return [STETH_ADDRESS, steth_equivalent]
    else:
        return [ZERO_ADDRESS, steth_equivalent]
