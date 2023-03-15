from defi_protocols import SushiSwap
from defi_protocols.constants import ETHEREUM, USDC_ETH, WETH_ETH
from defi_protocols.functions import get_node


SUSHISWAP_POOL_USDC_WETH = '0x397FF1542f962076d0BFE58eA045FfA2d347ACa0'
UNUSED_ADDRESS = '0xCafe7CceDfB2deBE0a49830D3C2777721E3728A5'

def test_get_lptoken_data():
    data = SushiSwap.get_lptoken_data(SUSHISWAP_POOL_USDC_WETH, 'latest', ETHEREUM)
    assert data['token0'] == USDC_ETH
    assert data['token1'] == WETH_ETH
    assert data['decimals'] == 18

def test_underlying_of_empty_address():
    data = SushiSwap.underlying(UNUSED_ADDRESS, SUSHISWAP_POOL_USDC_WETH, 'latest', ETHEREUM)
    assert data == [[USDC_ETH, 0.0, 0.0], [WETH_ETH, 0.0, 0.0]]

def test_get_pool_info_v1():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(web3, SUSHISWAP_POOL_USDC_WETH, block=16836190,
                                   blockchain=ETHEREUM, use_db=True)
    assert data['pool_info'] == {'poolId': 1, 'allocPoint': 8300}
    assert data['totalAllocPoint'] == 1639550

def test_get_pool_info_v2():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(web3, '0x269Db91Fc3c7fCC275C2E6f22e5552504512811c', block=16836190,
                                   blockchain=ETHEREUM, use_db=True)
    assert data['pool_info'] == {'poolId': 3, 'allocPoint': 5}
    assert data['totalAllocPoint'] == 1125

def test_get_pool_info_v2_without_db():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(web3, '0x269Db91Fc3c7fCC275C2E6f22e5552504512811c', block=16836190,
                                   blockchain=ETHEREUM, use_db=False)
    assert data['pool_info'] == {'poolId': 3, 'allocPoint': 5}
    assert data['totalAllocPoint'] == 1125
