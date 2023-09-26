import json

from defyes.prices.db_functions import TOKEN_MAPPING_FILE
from defyes.prices.prices import get_price


def test_get_price():
    price = get_price("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", 17628203, "ethereum", source="coingecko")
    assert price == (5.426491078544339, "coingecko", "ethereum")


def test_token_mapping_valid_json():
    with open(TOKEN_MAPPING_FILE) as f:
        json.load(f)
