from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes import compoundv3

WALLET_N1 = "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"


def test_underlying():
    block = 17151264
    underlying = compoundv3.underlying(WALLET_N1, EthereumTokenAddr.cUSDCv3, block, Chain.ETHEREUM)
    assert underlying == [[EthereumTokenAddr.USDC, Decimal("2208438.458228")]]


def test_get_all_rewards():
    block = 17836566
    all_rewards = compoundv3.get_all_rewards(WALLET_N1, EthereumTokenAddr.cUSDCv3, block, Chain.ETHEREUM)
    assert all_rewards == [[EthereumTokenAddr.COMP, Decimal("9.743306")]]


def test_get_protocol_data():
    block = 17836566
    p = compoundv3.get_protocol_data(Chain.ETHEREUM, WALLET_N1, block)
    assert p == {
        "protocol": "Compoundv3",
        "blockchain": "ethereum",
        "wallet": "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669",
        "block_id": 17836566,
        "positions_key": "commet_address",
        "positions": {
            "0xc3d688B66703497DAA19211EEdff47f25384cdc3": {
                "liquidity": {
                    "underlyings": [
                        {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "balance": Decimal("2221178.851613")}
                    ]
                },
                "unclaimed_rewards": [
                    {"address": "0xc00e94Cb662C3520282E6f5717214004A7f26888", "balance": Decimal("9.743306")}
                ],
            }
        },
        "version": 0,
    }

    block = 19134207
    wallet = "0x8f02a8ecd8734381795ff251360dbf1730cb46e6"
    p = compoundv3.get_protocol_data(Chain.ETHEREUM, wallet, block)
    assert p == {
        "protocol": "Compoundv3",
        "blockchain": "ethereum",
        "wallet": "0x8f02A8ecD8734381795FF251360DBf1730Cb46E6",
        "block_id": 19134207,
        "positions_key": "commet_address",
        "positions": {
            "0xc3d688B66703497DAA19211EEdff47f25384cdc3": {
                "unclaimed_rewards": [
                    {"address": "0xc00e94Cb662C3520282E6f5717214004A7f26888", "balance": Decimal("0.685091")}
                ],
                "collaterals": [
                    {
                        "balance": Decimal("5.76374023609637773"),
                        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    },
                    {
                        "balance": Decimal("4893.286852725209307716"),
                        "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                    },
                ],
                "borrowred": {
                    "balance": Decimal("24591.485098"),
                    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                },
            }
        },
        "version": 0,
    }
