from decimal import Decimal

from defi_protocols import Ankr
from defi_protocols.constants import ZERO_ADDRESS, ETHEREUM

ANKR_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'
WALLET = '0x5A6e41C8Ca7830D9ce5b3C8108fD163c7CC8D5E5'
BLOCKCHAIN = ETHEREUM

def test_underlying():
    block = 17293000
    underlying_unwrapped = Ankr.underlying(WALLET, block, BLOCKCHAIN, unwrapped=True)
    assert underlying_unwrapped == [[ZERO_ADDRESS, Decimal('269.06349805584043045')]]
    underlying_wrapped = Ankr.underlying(WALLET, block, BLOCKCHAIN, unwrapped=False)
    assert underlying_wrapped == [[ANKR_ADDR, Decimal('241.476225403906583644')]]
