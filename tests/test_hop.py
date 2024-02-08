from decimal import Decimal

from defabipedia import Chain

from defyes.protocols import hop

WALLET = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
HOP_DAI_LPTOKEN = "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F"


def test_get_protocol_data_for():
    block = 31781836
    p = hop.get_protocol_data_for(Chain.GNOSIS, WALLET, HOP_DAI_LPTOKEN, block)
    assert p == {
        "blockchain": "gnosis",
        "block_id": 31781836,
        "protocol": "Hop AMM",
        "version": 0,
        "wallet": "0x10E4597fF93cbee194F4879f8f1d54a370DB6969",
        "positions": {
            "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F": {
                "staked": {
                    "holdings": [
                        {
                            "address": "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F",
                            "balance": Decimal("378678.28363021317193841"),
                        }
                    ],
                    "underlyings": [
                        {
                            "balance": Decimal("261331.730956809988713531"),
                            "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                        },
                        {
                            "balance": Decimal("138833.916980042973172514"),
                            "address": "0xB1ea9FeD58a317F81eEEFC18715Dd323FDEf45c4",
                        },
                    ],
                    "unclaimed_rewards": [
                        {
                            "balance": Decimal("959.374383771847431411"),
                            "address": "0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC",
                        }
                    ],
                }
            }
        },
        "positions_key": "lptoken_address",
    }

    block = 32352866
    p = hop.get_protocol_data_for(Chain.GNOSIS, WALLET, HOP_DAI_LPTOKEN, block)
    assert p == {
        "blockchain": "gnosis",
        "block_id": 32352866,
        "protocol": "Hop AMM",
        "version": 0,
        "wallet": "0x10E4597fF93cbee194F4879f8f1d54a370DB6969",
        "positions": {
            "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F": {
                "staked": {
                    "holdings": [
                        {
                            "address": "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F",
                            "balance": Decimal("378678.28363021317193841"),
                        }
                    ],
                    "underlyings": [
                        {
                            "balance": Decimal("265030.2576089953432413"),
                            "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                        },
                        {
                            "balance": Decimal("135624.75533086420659118"),
                            "address": "0xB1ea9FeD58a317F81eEEFC18715Dd323FDEf45c4",
                        },
                    ],
                    "unclaimed_rewards": [
                        {
                            "balance": Decimal("20092.26993079498743539"),
                            "address": "0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC",
                        }
                    ],
                }
            }
        },
        "positions_key": "lptoken_address",
    }
