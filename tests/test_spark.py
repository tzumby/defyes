from decimal import Decimal

import pytest

from defyes import pretty
from defyes.constants import Chain
from defyes.protocols import spark
from defyes.types import Addr, Token

wallet = Addr(0x849D52316331967B6FF1198E5E32A0EB168D039D)
block_id = 17_772_457

DAI = Token(0x6B175474E89094C44DA98B954EEDEAC495271D0F, Chain.ETHEREUM)
GNO = Token(0x6810E776880C02933D47DB1B9FC05908E5386B96, Chain.ETHEREUM)

expected_positions = {
    GNO: {
        "holdings": [88_000_000000000000000000],
        "underlying": 88_000_000000000000000000,
    },
    DAI: {
        "holdings": [1_000_035_715961244421526907],
        "underlying": -1_000_035_715961244421526907,
    },
}

expected_positions_retro = {
    str(GNO): {
        "holdings": [
            {"address": "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F", "balance": 88_000_000000000000000000},
        ],
        "underlying": 88_000_000000000000000000,
    },
    str(DAI): {
        "holdings": [
            {"address": "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914", "balance": 1_000_035_715961244421526907},
        ],
        "underlying": -1_000_035_715961244421526907,
    },
}

expected_positions_retro_decimal = {
    str(GNO): {
        "holdings": [
            {"address": "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F", "balance": Decimal("88_000.0")},
        ],
        "underlying": Decimal("88_000.0"),
    },
    str(DAI): {
        "holdings": [
            {
                "address": "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914",
                "balance": Decimal("1_000_035.715961244421526907"),
            },
        ],
        "underlying": Decimal("-1_000_035.715961244421526907"),
    },
}


def expected_underlying_all(expected_positions):
    return {
        "block_id": block_id,
        "blockchain": "ethereum",
        "positions": expected_positions,
        "protocol": "Spark",
        "version": 0,
        "wallet": wallet,
    }


@pytest.fixture
def pdp():
    return spark.ProtocolDataProvider(Chain.ETHEREUM, block_id)


def test_underlying_all(pdp):
    ret = pdp.underlying_all(wallet)
    print()
    pretty.print(ret)
    pretty.jprint(ret)

    amount = ret["positions"][GNO]["holdings"][0]
    assert amount.token.symbol == "spGNO"
    assert amount.token == "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F"
    assert str(amount) == "88_000.0"
    assert amount == 88_000_000000000000000000

    amount = ret["positions"][DAI]["holdings"][0]
    assert amount.token.symbol == "variableDebtDAI"
    assert amount.token == "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914"
    assert str(amount) == "1_000_035.715961244421526907"
    assert amount == 1_000_035_715961244421526907

    assert ret == expected_underlying_all(expected_positions)


@pytest.mark.parametrize("decimal", [False, True], ids=["int", "decimal"])
def test_underlying_all_function(decimal):
    ret = spark.underlying_all(wallet, block_id, Chain.ETHEREUM, decimal=decimal)
    print()
    pretty.print(ret)
    pretty.jprint(ret)
    assert ret == expected_underlying_all(expected_positions_retro_decimal if decimal else expected_positions_retro)


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
