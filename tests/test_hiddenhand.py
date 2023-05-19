from unittest.mock import Mock
from decimal import Decimal

from defi_protocols import HiddenHand
from defi_protocols.constants import ETHEREUM

WALLET_N1 = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

HiddenHand.get_api_results = Mock()
#use data of 17-05-2023
api_result = [{'symbol': 'rpl', 'name': 'Rocket Pool', 'token': '0xd33526068d116ce69f19a9ee46f0bd304f21a51f', 'decimals': 18, 'chainId': 1, 'protocol': 'aura', 'claimable': '56.771231052533362388', 'value': 2835.7229910740416, 
            'claimMetadata': {'identifier': '0x329ffd9b41345bc4959db47e686a0416d414457adeaa66a22d5c5d79d6830e1b', 'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d', 'amount': '1882870279673552604832', 'merkleProof': ['xxx']}},
            {'symbol': 'aura', 'name': 'Aura Finance', 'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf', 'decimals': 18, 'chainId': 1, 'protocol': 'aura', 'claimable': '1493.272693434831511272', 'value': 2867.0835713948763, 
            'claimMetadata': {'identifier': '0x8eee07e6aecfd58a059e9c795e092747309d76151e2ab9562faf60b2d64673fd', 'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d', 'amount': '84806609263212397089872', 'merkleProof': ['xxx']}}, 
            {'symbol': 'usdc', 'name': 'USD Coin', 'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'decimals': 6, 'chainId': 1, 'protocol': 'aura', 'claimable': '3269.873946', 'value': 3269.873946, 
            'claimMetadata': {'identifier': '0x3f5a22cb83118980ed5887bc9ed2b8405706479ce22435bdf0b199c2192702ac', 'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d', 'amount': '126688248498', 'merkleProof': ['xxx']}}]
HiddenHand.get_api_results.return_value = api_result


end_result = {'protocol': 'HiddenHand', 'block': 'latest', 'positions': [{'position ID': 'aura', 'balances': 
        [{'token': '0xd33526068d116ce69f19a9ee46f0bd304f21a51f', 'balance': Decimal('56.771231052533362388')},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf', 'balance': Decimal('1493.272693434831511272')},
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'balance': Decimal('3269.873946')}]}]}


def test_underlying_all():
    data = HiddenHand.underlying_all(WALLET_N1,ETHEREUM)
    assert data == end_result