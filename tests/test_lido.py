from decimal import Decimal

import pytest
from defabipedia import Chain

from defyes import Lido
from defyes.constants import Address, ETHTokenAddr
from defyes.node import get_node

WALLET_N1 = "0x3591D9351C736Daa7867fA6629D3A10880d78b83"


@pytest.mark.parametrize("steth", [True, False])
def test_underlying(steth):
    block = 17059685
    node = get_node(Chain.ETHEREUM)

    underlying = Lido.underlying(WALLET_N1, block, web3=node, steth=steth)
    assert underlying == [[ETHTokenAddr.stETH if steth else Address.ZERO, Decimal("50.00010737587224903593918755")]]


@pytest.mark.parametrize("steth", [True, False])
def test_unwrap(steth):
    block = 17059674
    node = get_node(Chain.ETHEREUM)

    asset = Lido.unwrap(100, block, web3=node, steth=steth)
    assert asset == [ETHTokenAddr.stETH if steth else Address.ZERO, Decimal("111.912984654790019100")]
