from defabipedia import Chain

from defyes.protocols import hop

WALLET = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
HOP_DAI_LPTOKEN = "0x5300648b1cFaa951bbC1d56a4457083D92CFa33F"


def test_get_protocol_data_for():
    block = 31781836
    p = hop.get_protocol_data_for(Chain.GNOSIS, WALLET, HOP_DAI_LPTOKEN, block)
    assert p == {
        "holdings": ["378_678.28363021317193841*HOP-LP-DAI"],
        "underlyings": ["261_331.730956809988713531*WXDAI", "138_833.916980042973172514*hDAI"],
        "unclaimed_rewards": ["959.374383771847431411*HOP"],
        "financial_metrics": {},
    }
