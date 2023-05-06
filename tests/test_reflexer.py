from decimal import Decimal

from defi_protocols import Reflexer
from defi_protocols.constants import ETHTokenAddr


LPTOKEN_ADDR = '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9'
WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

def test_underlying():
    block = 16000000
    underlying = Reflexer.underlying(WALLET, LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('48390.17697598301237595034372')],
                          [ETHTokenAddr.WETH, Decimal('556.9148074791862518270731123')]]


def test_lptoken_underlying():
    block = 16000000
    underlying = Reflexer.balance_of_lptoken_underlying(WALLET, LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('0E+5')],
                          [ETHTokenAddr.WETH, Decimal('0.0000')]]


def test_pool_balances():
    block = 16000000
    underlying = Reflexer.pool_balance(LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('124449.6716793483356013894081')],
                          [ETHTokenAddr.WETH, Decimal('1432.271367359351870618411340')]]
