from pytest import raises
from defi_protocols.functions import get_web3_provider, get_node, get_decimals, get_symbol
from defi_protocols.constants import ETHEREUM, CVX_ETH, ETHTokenAddr, XDAI

def test_get_node():
    node = get_node(ETHEREUM)
    assert node

def test_get_node_of_unknown_network():
    raises(ValueError, get_node, 'unknown_network')

def test_get_symbol():
    symbol = get_symbol(ETHTokenAddr.DAI, blockchain=ETHEREUM, block=17380523)
    assert symbol == 'DAI'

    symbol = get_symbol("0x0000000000000000000000000000000000000000", blockchain=ETHEREUM, block=17380523)
    assert symbol == 'ETH'

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=ETHEREUM, block=17380523)
    assert symbol == 'ETH'

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=XDAI, block=17380523)
    assert symbol == 'XDAI'
