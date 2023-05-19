import pytest

from defi_protocols import Bancor
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, E_ADDRESS
from defi_protocols.functions import get_node

WALLET_N1 = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
WALLET_N2 = '0xc0167f4B1bb78912DF9920Bd146151942620Da15'

bnICHI_ADDR = '0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6'
bnETH_ADDR = '0x256Ed1d83E3e4EfDda977389A5389C3433137DDA'


def test_underlying():
    block = 17067718
    node = get_node(ETHEREUM, block)

    underlying = Bancor.underlying(bnICHI_ADDR, WALLET_N1, block, ETHEREUM, web3=node)
    assert underlying == [[ETHTokenAddr.ICHI, 44351.005182315], [ETHTokenAddr.BNT, 0.0]]
    underlying = Bancor.underlying(bnETH_ADDR, WALLET_N2, block, ETHEREUM, web3=node)
    assert underlying == [[E_ADDRESS, 0.14970330422829936], [ETHTokenAddr.BNT, 0.0]]


def test_underlying_all():
    block = 17067718
    node = get_node(ETHEREUM, block)

    underlying = Bancor.underlying_all(WALLET_N2, block, ETHEREUM, web3=node)
    assert underlying == [[[E_ADDRESS, 0.14970330422829936], [ETHTokenAddr.BNT, 0.0]], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                          [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]