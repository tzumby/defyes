from defi_protocols import Lido
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node


WALLET_N1 = '0x3591D9351C736Daa7867fA6629D3A10880d78b83'


def test_underlying():
    block = 17059674
    node = get_node(ETHEREUM, block)

    underlying = Lido.underlying(WALLET_N1, block, web3=node, steth=False)
    assert underlying == [[ZERO_ADDRESS, 50.00010737587225]]

    block = 17059685
    node = get_node(ETHEREUM, block)

    underlying = Lido.underlying(WALLET_N1, block, web3=node, steth=True)
    assert underlying == [[ETHTokenAddr.stETH, 50.00010737587225]]


def test_unwrap():
    block = 17059674
    node = get_node(ETHEREUM, block)

    asset = Lido.unwrap(100, block, web3=node)
    assert asset == [ZERO_ADDRESS, 111]

    asset = Lido.unwrap(100.0, block, web3=node, steth=True)
    assert asset == [ETHTokenAddr.stETH, 111.91298465479002]
