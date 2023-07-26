from pprint import PrettyPrinter

import pytest

from defyes.constants import Chain
from defyes.protocols import spark
from defyes.types import Addr, Token

wallet = Addr(0x849D52316331967B6FF1198E5E32A0EB168D039D)
block_id = 17_772_457

DAI = Token(0x6B175474E89094C44DA98B954EEDEAC495271D0F, "DAI")
GNO = Token(0x6810E776880C02933D47DB1B9FC05908E5386B96, "GNO")

expected_positions = {
    DAI: {
        "holdings": {
            "variable_debt_DAI": 1_000_035_715961244421526907,
        },
        "underlying": -1_000_035_715961244421526907,
    },
    GNO: {
        "holdings": {
            "sp_GNO": 88_000_000000000000000000,
        },
        "underlying": 88_000_000000000000000000,
    },
}

expected_underlying_all = {
    "block_id": 17_772_457,
    "blockchain": "ethereum",
    "positions": expected_positions,
    "protocol": "Spark",
    "version": 0,
    "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
}
pp = PrettyPrinter(indent=2, width=180, compact=True, underscore_numbers=True)


@pytest.fixture
def pdp():
    return spark.ProtocolDataProvider(Chain.ETHEREUM, block_id)


def test_underlying_all_function():
    ret = spark.underlying_all(wallet, block_id, Chain.ETHEREUM)
    assert ret == expected_underlying_all


def test_underlying_all(pdp):
    ret = pdp.underlying_all(wallet)
    assert ret == expected_underlying_all


def test_positions(pdp):
    assert dict(pdp.positions(wallet)) == expected_positions


def test_reserve_tokens_addresses(pdp):
    asset_tokens = list(pdp.assets_with_reserve_tokens)
    assert len(asset_tokens) == 8
    for asset, tokens in asset_tokens:
        assert isinstance(asset, str)
        assert isinstance(tokens.sp, str)
        assert isinstance(tokens.stable_debt, str)
        assert isinstance(tokens.variable_debt, str)
