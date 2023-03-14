from defi_protocols import SushiSwap
from defi_protocols.constants import ETHEREUM, USDC_ETH, WETH_ETH


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
