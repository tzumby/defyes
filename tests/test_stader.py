from decimal import Decimal

from defabipedia import Chain

from defyes.protocols import stader

WALLET = "0x4F2083f5fBede34C2714aFfb3105539775f7FE64"
ETHx = "0xa35b1b31ce002fbf2058d22f30f95d405200a15b"


def test_get_protocol_data_for():
    block = 19264497
    p = stader.get_protocol_data_for(Chain.ETHEREUM, WALLET, ETHx, block)
    assert p == {
        "blockchain": "ethereum",
        "block_id": 19264497,
        "protocol": "Stader",
        "version": 0,
        "wallet": "0x4F2083f5fBede34C2714aFfb3105539775f7FE64",
        "positions": {
            "0xA35b1B31Ce002FBF2058D22F30f95D405200A15b": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0xA35b1B31Ce002FBF2058D22F30f95D405200A15b",
                            "balance": Decimal("995.830893684182054684"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0x0000000000000000000000000000000000000000",
                            "balance": Decimal("1017.757772400597608194"),
                        }
                    ],
                }
            }
        },
        "positions_key": "lptoken_address",
    }
