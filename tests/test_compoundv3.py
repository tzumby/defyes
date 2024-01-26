from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes import compoundv3

WALLET_N1 = "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"
TOKEN_ADDRESS = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"


def test_underlying():
    block = 17151264
    underlying = compoundv3.underlying(WALLET_N1, TOKEN_ADDRESS, block, Chain.ETHEREUM)
    assert underlying == [[EthereumTokenAddr.USDC, Decimal("2208438.458228")]]


def test_get_all_rewards():
    block = 17836566
    all_rewards = compoundv3.get_all_rewards(WALLET_N1, TOKEN_ADDRESS, block, Chain.ETHEREUM)
    assert all_rewards == [[EthereumTokenAddr.COMP, Decimal("9.743306")]]
