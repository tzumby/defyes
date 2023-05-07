from decimal import Decimal
from defi_protocols import mStable
from defi_protocols.constants import ETHEREUM, ETHTokenAddr


WALLET = '0x83dE1603DF0249c0155e30c636598FEE5E11DBdc'
WALLET = '0x0BeC56dE373da44018b2B9f68842b7371CC3B8DB'
TOKEN_ADDR = '0x455fb969dc06c4aa77e7db3f0686cc05164436d2'


def test_underlying():
    block = 16294556
    block = 16473571
    underlying = mStable.underlying(TOKEN_ADDR, WALLET, block, blockchain=ETHEREUM)
    assert underlying == [[ETHTokenAddr.USDC, Decimal('0')]]
