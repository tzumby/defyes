import logging
import pytest
from decimal import Decimal

from defi_protocols import Agave, add_stderr_logger
from defi_protocols.constants import XDAI, AGVE_XDAI
from defi_protocols.functions import get_node, get_contract


add_stderr_logger(logging.DEBUG)


STK_AGAVE = '0x610525b415c1BFAeAB1a3fc3d85D87b92f048221'
TEST_WALLET_ADDRESS = '0xc4d46395c01aa86389d4216c2830167878d7cab8'
UNUSED_ADDRESS = '0xcafe6395c01aa86389d4216c2830167878d7cab8'
TEST_BLOCK = 27187881
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)

# 2023.03.29
TOP_WALLET_ADDRESS = '0xb4c575308221caa398e0dd2cdeb6b2f10d7b000a'
TOP_WALLET_W = \
    [['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83', 129855918919],
     ['0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d', 204984404799221030364433],
     ['0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2', 116756629133928213523],
     ['0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb', 816596478974281580761],
     ['0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252', 20774443],
     ['0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1', 282650106097633403696],
     ['0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d', 4922397761223675816108],
     ['0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 149615952]]


# https://gnosisscan.io/address/0x24dcbd376db23e4771375092344f5cbea3541fc0#readContract
# getAllReservesTokens
# 2023.03.29
RESERVES_TOKENS = \
    [('USDC', '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83'),
     ('WXDAI', '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d'),
     ('LINK', '0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2'),
     ('GNO', '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb'),
     ('WBTC', '0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252'),
     ('WETH', '0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1'),
     ('FOX', '0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d'),
     ('USDT', '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'),
     ('EURe', '0xcB444e90D8198415266c6a2724b7900fb12FC56E')]


def test_get_reserves_tokens():
    pdp_contract = get_contract(Agave.PDP_XDAI, XDAI, web3=WEB3, abi=Agave.ABI_PDP,
                                block=TEST_BLOCK)
    reserves_tokens = Agave.get_reserves_tokens(pdp_contract, TEST_BLOCK)
    assert reserves_tokens == [e[1] for e in RESERVES_TOKENS]


def test_get_reserves_tokens_balances():
    balances = Agave.get_reserves_tokens_balances(WEB3, TOP_WALLET_ADDRESS, TEST_BLOCK, XDAI, decimals=False)
    assert balances == TOP_WALLET_W


def test_get_data():
    SOME_WALLET_ADDRESS = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
    data = Agave.get_data(SOME_WALLET_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3)

    # We can't test xdai_price_usd because it fluctuates.
    expected = {'collateral_ratio': 0,
                'liquidation_ratio': 0,
                # 'xdai_price_usd': 1.00004,
                'collaterals': [],
                'debts': []}
    assert {k: data[k] for k in expected} == expected


def test_get_all_rewards():
    all_rewards = Agave.get_all_rewards(TEST_WALLET_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3, decimals=True)
    assert all_rewards == [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843',
                            Decimal('14.334056377962964551')]]


@pytest.mark.parametrize('reward', [True, False])
def test_underlying_all(reward):
    SOME_WALLET_ADDRESS = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
    ua = Agave.underlying_all(SOME_WALLET_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3, reward=reward)
    # FIXME: shape should not be dependent on arguments
    assert ua == {True: [[], [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 0.0]]],
                  False: []}[reward]


@pytest.mark.parametrize('apy', [True, False])
def test_get_apr(apy):
    TOKEN_ADDRESS = '0x3a97704a1b25F08aa230ae53B352e2e72ef52843'
    apr = Agave.get_apr(TOKEN_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3, apy=apy)
    # FIXME: make this more interesting:
    assert apr == {True: [{'metric': 'apy', 'type': 'supply', 'value': 0.0}, {'metric': 'apy', 'type': 'variable_borrow', 'value': 0.0}, {'metric': 'apy', 'type': 'stable_borrow', 'value': 0.0}],
                   False: [{'metric': 'apr', 'type': 'supply', 'value': 0.0}, {'metric': 'apr', 'type': 'variable_borrow', 'value': 0.0}, {'metric': 'apr', 'type': 'stable_borrow', 'value': 0.0}]}[apy]


# FIXME: This test seems to depend on fluctuating values
@pytest.mark.parametrize('apy', [True, False])
def test_get_staking_apr(apy):
    TOKEN_ADDRESS = '0x3a97704a1b25F08aa230ae53B352e2e72ef52843'
    stk_apr = Agave.get_staking_apr(TEST_BLOCK, XDAI, web3=WEB3, apy=apy)
    assert stk_apr == {True: [{'metric': 'apy', 'type': 'staking', 'value': 0.12741271642245144}],
                       False: [{'metric': 'apr', 'type': 'staking', 'value': 0.1199253794401285}]}[apy]


@pytest.mark.parametrize('wallet_address', [TEST_WALLET_ADDRESS, UNUSED_ADDRESS])
def test_get_staked(wallet_address):
    expected = {TEST_WALLET_ADDRESS: Decimal('103.630383543378402291'),
                UNUSED_ADDRESS: 0.0}[wallet_address]

    data = Agave.get_staked(wallet_address, block=TEST_BLOCK, blockchain=XDAI, web3=WEB3)
    assert data == [[AGVE_XDAI, expected]]

