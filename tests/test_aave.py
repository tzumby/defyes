from decimal import Decimal
from defi_protocols import Aave

from defi_protocols.constants import ETHEREUM, ETHTokenAddr


STK_AAVE = '0x4da27a545c0c5B758a6BA100e3a049001de870f5'
STK_ABPT = '0xa1116930326D21fB917d5A27F1E9943A9595fb47'
TEST_ADDRESS = '0xf929122994e177079c924631ba13fb280f5cd1f9'


def test_get_staking_balance():
    data = Aave.get_staked(TEST_ADDRESS,block=16870553,blockchain=ETHEREUM)
    assert data == [[ETHTokenAddr.AAVE, 11538.124991799179], [ETHTokenAddr.ABPT, 0.0]]

def test_get_apr():
    data = Aave.get_apr(ETHTokenAddr.DAI, block=16870553, blockchain=ETHEREUM)
    assert data == [
        {'metric': 'apr', 'type': 'supply', 'value': 0.0035380393235365103},
        {'metric': 'apr', 'type': 'variable_borrow', 'value': 0.01371866748498549},
        {'metric': 'apr', 'type': 'stable_borrow', 'value': 0.10685933374249275}]

def test_get_staking_apr():
    data = Aave.get_staking_apr(block=16870553, blockchain=ETHEREUM)
    assert data == [{'metric': 'apr', 'type': 'staking', 'value': Decimal('0.06083395929558314368366087980')}]

def test_underlying_all():
    data = Aave.underlying_all(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == [['0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599', -141.35367794],
                    ['0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F', 76289.38833267227],
                    ['0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', -291.885786],
                    ['0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272', 351227.5660308024],
                    ['0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84', 6612.667414298344]]

def test_get_data():
    data = Aave.get_data(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == {
        'collateral_ratio': 315.2041298065367,
        'liquidation_ratio': 122.2792858889704,
        'eth_price_usd': 1756.2,
        'collaterals': [
            {'token_address': '0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F',
             'token_amount': 76289.38833267227,
             'token_price_usd': 3.0891558},
            {'token_address': '0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272',
             'token_amount': 351227.5660308024,
             'token_price_usd': 1.6009054059164451},
            {'token_address': '0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84',
             'token_amount': 6612.667414298344,
             'token_price_usd': 1752.8773220566743}],
        'debts': [
            {'token_address': '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
             'token_amount': 141.35367794,
             'token_price_usd': 27804.195280199998},
            {'token_address': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
             'token_amount': 291.885786,
             'token_price_usd': 0.9937854059046765}]
    }

def test_get_all_rewards():
    data = Aave.get_all_rewards(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == [['0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9', 83.88802308439021]]
