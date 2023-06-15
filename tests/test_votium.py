from decimal import Decimal

import pytest

from defi_protocols import Votium

WALLET = '0x849d52316331967b6ff1198e5e32a0eb168d039d'


# Check if the output is a bool.
def test_check_claimed_or_unclaimed():
    index_number = 1404
    x = Votium.check_claimed_or_unclaimed(WALLET, index_number)
    assert isinstance(x, bool)


# Check output
def test_get_rewards_per_token():
    token_symbol = 'LDO'
    decimals = 18
    round_number = '0013'
    x = Votium.get_rewards_per_token(WALLET, token_symbol, decimals, round_number)
    if Votium.check_claimed_or_unclaimed(WALLET, 1675):
        assert x == Decimal(0)
    else:
        assert x == Decimal(439.9597422149969)


# TODO test for get all, it just runs get rewards per token for a list
def test_get_all_rewards(wallet):
    pass
