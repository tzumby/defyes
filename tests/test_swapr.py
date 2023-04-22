import pytest
from defi_protocols import Swapr
from defi_protocols.functions import get_node, get_contract
from defi_protocols.constants import XDAI, ETHEREUM, GNO_XDAI, WETH_XDAI

TEST_BLOCK = 27450341
TEST_WALLET = '0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f'
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)

# DXS is the lptoken for BER+GNO pair
DXS = '0x1Ad6A0cFF3870b252492597B557F3e61F130663D'
BER_XDAI = '0x05698e7346Ea67Cfb088f64Ad8962B18137d17c0'


# There is no point in testing:
# get_staking_rewards_contract
# It's just a switch


#FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
def test_get_distribution_contracts(campaigns, db):
    staking_rewards_contract = get_contract(Swapr.SRC_XDAI, XDAI, web3=WEB3, abi=Swapr.ABI_SRC, block=TEST_BLOCK)
    x = Swapr.get_distribution_contracts(WEB3, GNO_XDAI, staking_rewards_contract, campaigns, TEST_BLOCK, XDAI, db=db)
    assert x == []


def test_get_lptoken_data():
    x = Swapr.get_lptoken_data(DXS, TEST_BLOCK, XDAI, WEB3)
    expected =  {'decimals': 18,
                 'totalSupply': 94233751915117971705,
                 'token0': BER_XDAI,
                 'token1': GNO_XDAI,
                 'reserves': [1071822921647535396369, 8286413444006866465, 1677145545],
                 'kLast': 8880000000000000000000000000000000000000,
                 'virtualTotalSupply': 9.423513825757097e+19}
    assert {k: x[k] for k in expected} == expected


#FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
def test_get_all_rewards(campaigns, db):
    x = Swapr.get_all_rewards(TEST_WALLET, DXS, TEST_BLOCK, XDAI, WEB3,
                              decimals=True, campaigns=campaigns, distribution_contracts=None, db=db)
    assert x == []


#FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
def test_underlying(campaigns, db):
    x = Swapr.underlying(TEST_WALLET, DXS, TEST_BLOCK, XDAI, WEB3,
                         decimals=True, reward=False, campaigns=campaigns, db=db)
    assert x == [[BER_XDAI, 1071.807153499413, 0.0],
                 [GNO_XDAI, 8.28629153824058, 0.0]]


def test_pool_balances():
    x = Swapr.pool_balances(DXS, TEST_BLOCK, XDAI, WEB3, decimals=True)
    assert x == [[BER_XDAI, 1071.8229216475354],
                 [GNO_XDAI, 8.286413444006866]]


def test_swap_fees():
    x = Swapr.swap_fees(DXS, TEST_BLOCK - 100, 27568826, XDAI, WEB3, decimals=True)
    assert x['swaps'] == [{'block': 27494581, 'token': BER_XDAI, 'amount': 0.25},
                          {'block': 27494618, 'token': BER_XDAI, 'amount': 1.5625},
                          {'block': 27494972, 'token': GNO_XDAI, 'amount': 0.002537125747349638},
                          {'block': 27507943, 'token': GNO_XDAI, 'amount': 1.0825598350382856e-05},
                          {'block': 27508016, 'token': BER_XDAI, 'amount': 0.0024973853361934853},
                          {'block': 27508197, 'token': GNO_XDAI, 'amount': 1.075289768548977e-05},
                          {'block': 27510159, 'token': BER_XDAI, 'amount': 0.1041406249942838}]


@pytest.mark.skip('This takes forever')
def test_update_db():
    Swapr.update_db()
    assert True
