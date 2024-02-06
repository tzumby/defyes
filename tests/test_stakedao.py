from decimal import Decimal

from defabipedia import Chain

from defyes.protocols import stakedao

sdCRV = "0xD1b5651E55D4CeeD36251c61c50C889B36F6abB5"
WALLET = "0x205e795336610f5131Be52F09218AF19f0f3eC60"
BLOCK = 19141836


def test_gauge_rewards():
    gauge_addr = "0x7f50786A0b15723D741727882ee99a0BF34e3466"
    gauge = stakedao.Gauge(Chain.ETHEREUM, BLOCK, gauge_addr)

    rewards = gauge.get_rewards(WALLET)
    assert rewards == ["2.133800353186004506*SDT", "2_017.825468905329065068*3Crv", "310.568028118674492999*CRV"]


def test_protocol_data_for():
    p = stakedao.get_protocol_data_for(Chain.ETHEREUM, WALLET, sdCRV, BLOCK)
    assert p == {
        "blockchain": "ethereum",
        "block_id": 19141836,
        "protocol": "Stake DAO",
        "version": 0,
        "wallet": "0x205e795336610f5131Be52F09218AF19f0f3eC60",
        "positions": {
            "0xD1b5651E55D4CeeD36251c61c50C889B36F6abB5": {
                "staked": {
                    "holdings": [
                        {
                            "address": "0xD1b5651E55D4CeeD36251c61c50C889B36F6abB5",
                            "balance": Decimal("1052794.333008235689952123"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0xD533a949740bb3306d119CC777fa900bA034cd52",
                            "balance": Decimal("1052794.333008235689952123"),
                        }
                    ],
                    "unclaimed_rewards": [
                        {
                            "balance": Decimal("2.133800353186004506"),
                            "address": "0x73968b9a57c6E53d41345FD57a6E6ae27d6CDB2F",
                        },
                        {
                            "balance": Decimal("2017.825468905329065068"),
                            "address": "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490",
                        },
                        {
                            "balance": Decimal("310.568028118674492999"),
                            "address": "0xD533a949740bb3306d119CC777fa900bA034cd52",
                        },
                    ],
                }
            }
        },
        "positions_key": "lptoken_address",
    }
