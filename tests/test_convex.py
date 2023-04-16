import logging
from decimal import Decimal

from defi_protocols import Convex, add_stderr_logger
from defi_protocols.functions import get_node, get_contract
from defi_protocols.constants import ETHEREUM, X3CRV_ETH, CRV_ETH, DAI_ETH, USDC_ETH, USDT_ETH, CVX_ETH


add_stderr_logger(logging.DEBUG)
TEST_BLOCK = 16993460
TEST_WALLET = '0xF929122994E177079c924631bA13Fb280F5CD1f9'
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)


def test_get_pool_info():
    x = Convex.get_pool_info(X3CRV_ETH, TEST_BLOCK)
    assert x == ['0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490',
                 '0x30D9410ED1D5DA1F6C8391af5338C93ab8d4035C',
                 '0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A',
                 '0x689440f2Ff927E1f24c72F1087E1FAF471eCe1c8',
                 '0x0000000000000000000000000000000000000000', False]


def test_get_rewards():
    pool_info = Convex.get_pool_info(X3CRV_ETH, TEST_BLOCK)
    rw_contract = get_contract(pool_info[3], ETHEREUM,
                               web3=WEB3, abi=Convex.ABI_REWARDS,
                               block=TEST_BLOCK)
    x = Convex.get_rewards(WEB3, rw_contract, TEST_WALLET, TEST_BLOCK,
                           ETHEREUM, decimals=False)
    # FIXME: interestingficate!
    assert x == ['0xD533a949740bb3306d119CC777fa900bA034cd52', 0.0]


def test_get_extra_rewards():
    pool_info = Convex.get_pool_info(X3CRV_ETH, TEST_BLOCK)
    rw_contract = get_contract(pool_info[3], ETHEREUM,
                               web3=WEB3, abi=Convex.ABI_REWARDS,
                               block=TEST_BLOCK)
    x = Convex.get_extra_rewards(WEB3, rw_contract, TEST_WALLET, TEST_BLOCK,
                                 ETHEREUM, decimals=False)
    # FIXME: interestingficate!
    assert x == []


def test_get_cvx_mint_amount():
    x = Convex.get_cvx_mint_amount(WEB3, False, TEST_BLOCK, ETHEREUM, decimals=False)
    assert x == ['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]


def test_get_all_rewards():
    x = Convex.get_all_rewards(TEST_WALLET, X3CRV_ETH, TEST_BLOCK, ETHEREUM,
                               WEB3, False, None)
    assert x == [['0xD533a949740bb3306d119CC777fa900bA034cd52', 0.0],
                 ['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]


def test_get_locked():
    x = Convex.get_locked(TEST_WALLET, TEST_BLOCK, ETHEREUM,
                          WEB3, reward=False, decimals=False)
    assert x == [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]


def test_get_staked():
    x = Convex.get_staked(TEST_WALLET, TEST_BLOCK, ETHEREUM,
                          WEB3, reward=False, decimals=False)
    assert x == [['0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B', 0.0]]


def test_underlying():
    # (wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True, no_curve_underlying=False) 
    x = Convex.underlying(TEST_WALLET, X3CRV_ETH, TEST_BLOCK, ETHEREUM,
                          WEB3, reward=False, decimals=False,
                          no_curve_underlying=False)
    assert x == [['0x6B175474E89094C44Da98b954EedeAC495271d0F', Decimal('0')],
                 ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', Decimal('0')],
                 ['0xdAC17F958D2ee523a2206206994597C13D831ec7', Decimal('0')]]


def test_pool_balances():
    # (lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True) 
    x = Convex.pool_balances(X3CRV_ETH, TEST_BLOCK, ETHEREUM,
                             WEB3, decimals=False)
    assert x == [['0x6B175474E89094C44Da98b954EedeAC495271d0F',
                            Decimal('165857824629254122209119338')],
                 ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
                            Decimal('175604425510732')],
                 ['0xdAC17F958D2ee523a2206206994597C13D831ec7',
                            Decimal('92743777795510')]]


# FIXME: This test has unaceptable side effects!
def test_update_db():
    Convex.update_db()
    assert True
