from defi_protocols import UniswapV3
from defi_protocols.uniswapv3helper import LiquidityPosition
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node
from decimal import Decimal


WALLET_N1 = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
WALLET_N2 = '0x0EFcCBb9E2C09Ea29551879bd9Da32362b32fc89'
NFT_ID = 358770


def test_underlying():
    block = 17094489
    node = get_node(ETHEREUM, block)

    uniswapv3 = UniswapV3.underlying(WALLET_N1, NFT_ID, block, ETHEREUM, web3=node, fee=True)
    assert uniswapv3 == [[ETHTokenAddr.GNO, 98419.15638388108], [ETHTokenAddr.WETH, 2210.998677615111]]

    uniswapv3 = UniswapV3.underlying(WALLET_N1, NFT_ID, block, ETHEREUM, web3=node, decimals=False, fee=True)
    assert uniswapv3 == [[ETHTokenAddr.GNO, 98419156383881089964338], [ETHTokenAddr.WETH, 2210998677615110963219]]


def test_allnfts():
    block = 17094489
    node = get_node(ETHEREUM, block)

    nfts = UniswapV3.allnfts(WALLET_N1, block, ETHEREUM, node)
    assert nfts == [185085, 186529, 189493, 214704, 214707, 214716, 218573,
                    220361, 217714, 286920, 339884, 346143, 358770, 415282]


def test_underlying_all():
    block = 17119477

    balances = UniswapV3.underlying_all(WALLET_N2, block, ETHEREUM, fee=True)
    assert balances == [[[ETHTokenAddr.WBTC, 7.755961341942962e-06], [ETHTokenAddr.WETH, 0.001896950944013546]],
                        [[ETHTokenAddr.WETH, 0.0005397922732214861], [ETHTokenAddr.sETH2, 0.001391854480130107]],
                        [[ETHTokenAddr.WBTC, 8.020662597920984], [ETHTokenAddr.WETH, 194.4352083634992]]]


def test_get_rate():
    block = 17094489
    node = get_node(ETHEREUM, block)

    position_nft = UniswapV3.NFTPosition(NFT_ID, ETHEREUM, block, node, decimals=True)
    assert UniswapV3.get_rate_uniswap_v3(position_nft.token0,
                                         position_nft.token1,
                                         block,
                                         ETHEREUM,
                                         node,
                                         UniswapV3.FeeAmount.MEDIUM) == 0.05737047195982491

def test_get_fee():
    block = 17094489
    node = get_node(ETHEREUM, block)

    position_nft = UniswapV3.NFTPosition(NFT_ID, ETHEREUM, block, node, decimals=True)

    fees = UniswapV3.get_fee(NFT_ID, block, web3=node, blockchain=ETHEREUM, decimals=True)
    assert fees == [['0x6810e776880C02933D47DB1b9fc05908e5386b96', Decimal('474.998434375840983379')], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', Decimal('25.927112063507954904')]]

    fees = UniswapV3.get_fee(NFT_ID, block, web3=node, blockchain=ETHEREUM, decimals=False)
    assert fees == [['0x6810e776880C02933D47DB1b9fc05908e5386b96', 474998434375840983379], ['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 25927112063507954904]]

