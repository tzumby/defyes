from pytest import raises
from defi_protocols.functions import get_web3_provider, get_node, get_decimals
from defi_protocols.constants import ETHEREUM, CVX_ETH

def test_get_web3_provider():
    web3 = get_web3_provider('http://rpc.foo.com')
    assert web3

def test_get_web3_provider_without_correct_uri():
    raises(ValueError, get_web3_provider, 'first')

def test_get_node():
    node = get_node(ETHEREUM)
    assert node

def test_get_node_of_unknown_network():
    raises(ValueError, get_node, 'unknown_network')

def test_get_decimals():
    get_decimals(CVX_ETH, ETHEREUM)