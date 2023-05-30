from decimal import Decimal

from defi_protocols import Ankr
from defi_protocols.constants import ZERO_ADDRESS, ETHEREUM

ANKR_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'
TOKEN_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'
WALLET = '0x5A6e41C8Ca7830D9ce5b3C8108fD163c7CC8D5E5'
BLOCKCHAIN = ETHEREUM

def test_underlying():
    block = 17293000
    underlying = Ankr.underlying(WALLET, block, BLOCKCHAIN)
    assert underlying == [[ZERO_ADDRESS, Decimal('269.06349805584043045')]]
