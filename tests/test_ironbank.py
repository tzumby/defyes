import pytest

from defi_protocols import IronBank
from defi_protocols.constants import OPTIMISM
from defi_protocols.functions import get_node


# 2023.04.27
TEST_BLOCK = 94882677
TEST_WALLET = '0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC'
WEB3 = get_node(blockchain=OPTIMISM, block=TEST_BLOCK)

iUSDC = '0x1d073cf59Ae0C169cbc58B6fdD518822ae89173a'
USDC = '0x7F5c764cBc14f9669B88837ca1490cCa17c31607'
IB = '0x00a35FD824c717879BF370E70AC6868b95870Dfb'
veIB = '0x707648dfbF9dF6b0898F78EdF191B85e327e0e05'


def test_get_itoken_data():
    data = IronBank.get_itoken_data(iUSDC, TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, None)
    expected = {'underlying': USDC,
                'decimals': 8,
                'borrowBalanceStored': 0,
                'balanceOf': 37470207787145,
                'exchangeRateStored': 101609986612647}
    assert {k: data[k] for k in expected} == expected


def test_get_all_rewards():
    x = IronBank.get_all_rewards(TEST_WALLET, iUSDC, TEST_BLOCK, OPTIMISM, WEB3, True, None)
    assert x == [[IB, 0.0]]


def test_all_rewards():
    x = IronBank.all_rewards(TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, True)
    assert x == [[IB, 0.0]]


# FIXME: fluctuating balances
def test_get_locked():
    x = IronBank.get_locked(TEST_WALLET, TEST_BLOCK, OPTIMISM, 302, WEB3, False, decimals=False)
    assert x == [[veIB, pytest.approx(5.4181e22, rel=1e-3)],
                 [IB, pytest.approx(6.98e22, rel=1e-3)]]


def test_underlying():
    x = IronBank.underlying(TEST_WALLET, USDC, TEST_BLOCK, OPTIMISM, WEB3, True, False)
    assert x == [[USDC, 3807.3473116249047, 0]]


def test_underlying_all():
    x = IronBank.underlying_all(TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, True, False)
    assert x == [[USDC, 3807.3473116249047, 0]]


def test_unwrap():
    x = IronBank.unwrap(198489.26169641, iUSDC, TEST_BLOCK, OPTIMISM, WEB3, True)
    assert x == [USDC, 2016.8491223726407]
