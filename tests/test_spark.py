from decimal import Decimal

import pytest

from defi_protocols import Spark as spark
from defi_protocols.constants import ETHEREUM
from future_defyes import pretty
from future_defyes.types import Addr, Token

wallet = Addr(0x849D52316331967B6FF1198E5E32A0EB168D039D)
block_id = 17_772_457

DAI = Token(0x6B175474E89094C44DA98B954EEDEAC495271D0F, "DAI")
GNO = Token(0x6810E776880C02933D47DB1B9FC05908E5386B96, "GNO")

expected_positions = {
    GNO: {
        "holdings": {
            "sp_GNO": 88_000_000000000000000000,
        },
        "underlying": 88_000_000000000000000000,
    },
    DAI: {
        "holdings": {
            "variable_debt_DAI": 1_000_035_715961244421526907,
        },
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


expected_get_data = {
    "collateral_ratio": Decimal("1016.357510595627631280679422"),
    "liquidation_ratio": Decimal("400"),
    "native_token_price_usd": Decimal("1857.8255"),
    "collaterals": [
        {
            "token_address": "0x6810e776880C02933D47DB1b9fc05908e5386b96",
            "token_amount": Decimal("88000.0"),
            "token_price_usd": Decimal("115.48774675"),
            "token_symbol": "GNO",
        }
    ],
    "debts": [
        {
            "token_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "token_amount": Decimal("1000035.715961244421526907"),
            "token_price_usd": Decimal("0.9999"),
            "token_symbol": "DAI",
        }
    ],
}


expected_get_data_int = {
    "collateral_ratio": Decimal("1016.357510595627631280679422"),
    "liquidation_ratio": Decimal("400"),
    "native_token_price_usd": Decimal("1857.8255"),
    "collaterals": [
        {
            "token_address": "0x6810e776880C02933D47DB1b9fc05908e5386b96",
            "token_amount": 88_000_000000000000000000,
            "token_price_usd": Decimal("115.48774675"),
            "token_symbol": "GNO",
        }
    ],
    "debts": [
        {
            "token_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "token_amount": 1_000_035_715961244421526907,
            "token_price_usd": Decimal("0.9999"),
            "token_symbol": "DAI",
        }
    ],
}


@pytest.fixture
def pdp():
    return spark.ProtocolDataProvider(ETHEREUM, block_id)


def test_underlying_all(pdp):
    ret = pdp.underlying_all(wallet)
    print()
    pretty.print(ret)
    pretty.jprint(ret)

    sp_GNO = ret["positions"][GNO]["holdings"]["sp_GNO"]
    assert str(sp_GNO) == "88_000.0"
    assert sp_GNO == 88_000_000000000000000000
    assert sp_GNO.addr == "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F"

    variable_debt_DAI = ret["positions"][DAI]["holdings"]["variable_debt_DAI"]
    assert str(variable_debt_DAI) == "1_000_035.715961244421526907"
    assert variable_debt_DAI == 1_000_035_715961244421526907
    assert variable_debt_DAI.addr == "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914"

    assert ret == expected_underlying_all(expected_positions)


decimal = pytest.mark.parametrize("decimal", [False, True], ids=["int", "decimal"])


@decimal
def test_underlying_all_function(decimal):
    ret = spark.underlying_all(wallet, block_id, ETHEREUM, decimals=decimal)
    print()
    pretty.print(ret)
    pretty.jprint(ret)
    expected = expected_underlying_all(expected_positions_retro_decimal if decimal else expected_positions_retro)
    expected["decimals"] = decimal
    assert ret == expected


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


@decimal
def test_get_data(decimal):
    ret = spark.get_data(wallet, block_id, ETHEREUM, decimals=decimal)
    print()
    pretty.print(ret)
    pretty.jprint(ret)
    assert ret == expected_get_data if decimal else expected_get_data_int
