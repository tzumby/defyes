from decimal import Decimal

import pytest
from karpatkit.constants import Chain

from defyes.protocols import stakewisev3


def test_reduce_osETH():
    result = stakewisev3.reduce_osETH(1231231, Chain.ETHEREUM, 19639409, False)
    assert result == ("0x0000000000000000000000000000000000000000", Decimal("1247742.592152337891407091"))


def test_reduce_osETH_invalid_blockchain():
    with pytest.raises(ValueError, match="Currently only Ethereum is supported"):
        stakewisev3.reduce_osETH(1231231, "invalid_blockchain", 19639409, False)
