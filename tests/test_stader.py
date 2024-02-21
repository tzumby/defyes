from decimal import Decimal

from defabipedia import Chain

from defyes.protocols import stader

WALLET = "0x4F2083f5fBede34C2714aFfb3105539775f7FE64"
ETHx = "0xa35b1b31ce002fbf2058d22f30f95d405200a15b"


def test_get_protocol_data_for():
    block = 19264497
    p = stader.get_protocol_data_for(Chain.ETHEREUM, WALLET, ETHx, block)
    assert p == {'holdings': ["995.830893684182054684*ETHx"], 'underlyings': ["1_017.757772400597608194*ETH"], 'unclaimed_rewards': [], 'financial_metrics': {}}
