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
        "holdings": ["1_052_794.333008235689952123*sdCRV"],
        "underlyings": ["1_052_794.333008235689952123*CRV"],
        "unclaimed_rewards": [
            "2.133800353186004506*SDT",
            "2_017.825468905329065068*3Crv",
            "310.568028118674492999*CRV",
        ],
        "financial_metrics": {},
    }
