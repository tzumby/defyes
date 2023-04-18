
from defi_protocols import Honeyswap, add_stderr_logger
from defi_protocols.functions import get_node
from defi_protocols.constants import XDAI, WETH_XDAI, GNO_XDAI


TEST_BLOCK = 27450341
TEST_WALLET = '0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f'
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)

UNIv2 = '0x28dbd35fd79f48bfa9444d330d14683e7101d817'


def test_get_lptoken_data():
    data = Honeyswap.get_lptoken_data(UNIv2, TEST_BLOCK, XDAI, WEB3, 1, 0)
    expected =  {'decimals': 18,
                 'totalSupply': 2780438593422870570963,
                 'token0': WETH_XDAI,
                 'token1': GNO_XDAI,
                 'reserves': [697389190335766422886,
                              11931109898533386964234,
                              1681509230],
                 'kLast': 8320457320306632575150389158633998324068504,
                 'virtualTotalSupply': 2.780443320502662e+21}
    assert expected == {k: data[k] for k in expected}


def test_underlying():
    x = Honeyswap.underlying(TEST_WALLET, UNIv2, TEST_BLOCK, XDAI,
                             WEB3, 1, 0, True)
    assert x == [[WETH_XDAI, 697.3869748255132],
                 [GNO_XDAI, 11931.07199502602]]


def test_pool_balances():
    x = Honeyswap.pool_balances(UNIv2, TEST_BLOCK, XDAI, WEB3,
                                1, 0, decimals=True)
    assert x == [[WETH_XDAI, 697.3891903357664],
                 [GNO_XDAI, 11931.109898533387]]


def test_swap_fees():
    x = Honeyswap.swap_fees(UNIv2, TEST_BLOCK-100, TEST_BLOCK, XDAI, WEB3,
                            1, 0, decimals=True)
    assert x == {'swaps': []}
