import pytest
import logging

from defi_protocols.functions import get_node
from defi_protocols.constants import ETHEREUM, X3CRV_ETH, CRV_ETH, DAI_ETH, USDC_ETH, USDT_ETH
from defi_protocols import Curve, add_stderr_logger


_h = add_stderr_logger(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(_h)

# 2023.04.06
TEST_BLOCK = 16993460
TEST_WALLET = '0xf929122994e177079c924631ba13fb280f5cd1f9'

# DAI USDC USDT Curve Pool
CURVE_3POOL = '0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7'
CURVE_3POOL_GAUGE = '0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A'

WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)


@pytest.mark.parametrize('_id', [0, 3, 5, 6])
def test_get_registry_contract(_id):
    rc = Curve.get_registry_contract(WEB3, _id, TEST_BLOCK, ETHEREUM)
    # I'm just testing it does not break
    assert True


def test_get_lptoken_data():
    lpt_data = Curve.get_lptoken_data(X3CRV_ETH, TEST_BLOCK, ETHEREUM, web3=WEB3)
    expected = {'minter': None, 'decimals': 18, 'totalSupply': 423390670620160177728525799}
    assert expected == {k: lpt_data[k] for k in expected}


def test_get_pool_address():
    # TODO: this function has an intricate 'if' combination
    pa = Curve.get_pool_address(WEB3, X3CRV_ETH, TEST_BLOCK, ETHEREUM)
    assert pa == CURVE_3POOL


def test_get_pool_gauge_address():
    pga = Curve.get_pool_gauge_address(WEB3, CURVE_3POOL, X3CRV_ETH, TEST_BLOCK, ETHEREUM)
    assert pga == CURVE_3POOL_GAUGE


def test_get_gauge_version():
    # TODO: test for all versions
    # ChildGauge
    # LiquidityGaugeV5
    # LiquidityGaugeV4
    # LiquidityGaugeV3
    # LiquidityGaugeV2
    # LiquidityGaugeReward
    # RewardsOnlyGauge
    
    gv = Curve.get_gauge_version(CURVE_3POOL_GAUGE, TEST_BLOCK, ETHEREUM, web3=WEB3, only_version=True)
    assert gv == 'LiquidityGauge'


def test_get_pool_data():
    pd = Curve.get_pool_data(WEB3, CURVE_3POOL, TEST_BLOCK, ETHEREUM)
    expected = {'is_metapool': False,
                'coins': {0: DAI_ETH,
                          1: USDC_ETH,
                          2: USDT_ETH}}
    assert expected == {k: pd[k] for k in expected}


def test_get_all_rewards():
    rewards = Curve.get_all_rewards(TEST_WALLET, X3CRV_ETH, TEST_BLOCK, ETHEREUM,
                                    web3=WEB3, decimals=False)
    # FIXME: why decimals=False gives this?:
    # It should be an Int!
    assert rewards == [[CRV_ETH, 1.2062444658284873e+20]]


@pytest.mark.parametrize('reward', [True, False])
def test_underlying(reward):
    u = Curve.underlying(TEST_WALLET, X3CRV_ETH, TEST_BLOCK, ETHEREUM, web3=WEB3,
                         reward=reward)
    print(u) 
    expected = [[DAI_ETH, 0.0, 0.0],
                [USDC_ETH, 0.0, 0.0],
                [USDT_ETH, 0.0, 0.0]]
    # FIXME: shape should not depend on args
    if reward:
        expected = [expected, [[CRV_ETH, 120.62444658284873]]]

    assert u == expected


@pytest.mark.parametrize('lptoken_amount', [0, 10])
def test_unwrap(lptoken_amount):
    u = Curve.unwrap(lptoken_amount, X3CRV_ETH, TEST_BLOCK, ETHEREUM, web3=WEB3)

    expected = {0:
                      [[DAI_ETH, 0.0],
                      [USDC_ETH, 0.0],
                      [USDT_ETH, 0.0]],
                10:
                      [[DAI_ETH, 3.9173546855571995],
                      [USDC_ETH, 4.147544963364351],
                      [USDT_ETH, 2.1904608756716426]],
                }
    assert u == expected[lptoken_amount]


def test_pool_balances():
    pb = Curve.pool_balances(X3CRV_ETH, TEST_BLOCK, ETHEREUM, web3=WEB3)
    assert pb == [[DAI_ETH, 165857824.62925413],
                  [USDC_ETH, 175604425.510732],
                  [USDT_ETH, 92743777.79551]]


def test_swap_fees():
    sf = Curve.swap_fees(X3CRV_ETH, TEST_BLOCK-10, TEST_BLOCK, ETHEREUM, web3=WEB3)
    print(sf)
    assert sf == {'swaps': []}


@pytest.mark.skip('web3.exceptions.ABIFunctionNotFound')
@pytest.mark.parametrize('apy', [False, True])
def test_get_base_apr(apy):
    x = Curve.get_base_apr(X3CRV_ETH, ETHEREUM, TEST_BLOCK, web3=WEB3, apy=apy)
    print(x)
    assert True


@pytest.mark.skip('web3.exceptions.ABIFunctionNotFound')
@pytest.mark.parametrize('apy', [False, True])
def test_swap_fees_v2(apy):
    sf = Curve.swap_fees_v2(X3CRV_ETH, ETHEREUM, TEST_BLOCK, web3=WEB3, apy=apy)
    print(sf)
    assert True


@pytest.mark.skip('web3.exceptions.ABIFunctionNotFound')
def test_get_swap_fees_APR():
    sf = Curve.get_swap_fees_APR(X3CRV_ETH, ETHEREUM, TEST_BLOCK, web3=WEB3)
    print(sf)
    assert True
