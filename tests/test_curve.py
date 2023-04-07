import pytest
import logging

from defi_protocols.functions import get_node
from defi_protocols.constants import ETHEREUM, X3CRV_ETH, CRV_ETH
from defi_protocols import Curve, add_stderr_logger


logger = logging.getLogger(__name__)
add_stderr_logger(logging.DEBUG)

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
                'coins': {0: '0x6B175474E89094C44Da98b954EedeAC495271d0F',
                          1: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                          2: '0xdAC17F958D2ee523a2206206994597C13D831ec7'}}
    assert expected == {k: pd[k] for k in expected}


def test_get_all_rewards():
    rewards = Curve.get_all_rewards(TEST_WALLET, X3CRV_ETH, TEST_BLOCK, ETHEREUM,
                                    web3=WEB3, decimals=False)
    # FIXME: why decimals=False gives this?:
    assert rewards == [[CRV_ETH, 1.2062444658284873e+20]]


# Pending tests:
#   underlying
#   unwrap
#   pool_balances
#   swap_fees
#   get_base_apr
#   swap_fees_v2
#   get_swap_fees_APR
