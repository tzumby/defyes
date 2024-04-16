# FILEPATH: /Users/ubabe/Documents/defyes/tests/test_init.py

from decimal import Decimal

import pytest

from defyes.protocols.coinbase import reduce_cbETH


def test_reduce_cbETH():
    result = reduce_cbETH(10000, "ethereum", 19661532)
    assert result == ("0x0000000000000000000000000000000000000000", Decimal("10689.76237590522102"))


def test_reduce_cbETH_invalid_blockchain():
    with pytest.raises(ValueError, match="Currently only Ethereum is supported"):
        reduce_cbETH(10000, "invalid_blockchain", 19661532)
