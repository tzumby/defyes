import logging
import pytest

from defi_protocols import Agave, add_stderr_logger
from defi_protocols.constants import XDAI
from defi_protocols.functions import get_node, get_contract


add_stderr_logger(logging.DEBUG)

STK_AGAVE = '0x610525b415c1BFAeAB1a3fc3d85D87b92f048221'
TEST_WALLET_ADDRESS = '0xc4d46395c01aa86389d4216c2830167878d7cab8'
UNUSED_ADDRESS = '0xcafe6395c01aa86389d4216c2830167878d7cab8'
TEST_BLOCK = 27038905

WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)


def test_get_reserves_tokens():
    pdp_contract = get_contract(Agave.PDP_XDAI, XDAI, web3=WEB3, abi=Agave.ABI_PDP,
                                block=TEST_BLOCK)
    reserves_tokens = Agave.get_reserves_tokens(pdp_contract, TEST_BLOCK)
    assert reserves_tokens == ['0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83',
                               '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d',
                               '0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2',
                               '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                               '0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252',
                               '0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1',
                               '0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d',
                               '0x4ECaBa5870353805a9F068101A40E0f32ed605C6',
                               '0xcB444e90D8198415266c6a2724b7900fb12FC56E']


def test_get_reserves_tokens_balances():
    # FIXME: we should test with a more interesting wallet
    balances = Agave.get_reserves_tokens_balances(WEB3, TEST_WALLET_ADDRESS, TEST_BLOCK, XDAI)
    print(balances)
    assert balances == []


def test_get_data():
    SOME_WALLET_ADDRESS = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
    data = Agave.get_data(SOME_WALLET_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3)
    print(data)
    # FIXME: this test is passing for the wrong reasons
    assert data is None


def test_get_all_rewards():
    all_rewards = Agave.get_all_rewards(TEST_WALLET_ADDRESS, TEST_BLOCK, XDAI, web3=WEB3)
    assert all_rewards == [['0x3a97704a1b25F08aa230ae53B352e2e72ef52843', 14.019150785520575]]


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


@pytest.mark.parametrize('apy', [True, False])
def test_get_staking_apr(apy):
    TOKEN_ADDRESS = '0x3a97704a1b25F08aa230ae53B352e2e72ef52843'
    stk_apr = Agave.get_staking_apr(TEST_BLOCK, XDAI, web3=WEB3, apy=apy)
    assert stk_apr == {True: [{'metric': 'apy', 'type': 'staking', 'value': 0.1286313524174969}],
                       False: [{'metric': 'apr', 'type': 'staking', 'value': 0.12100570935407559}]}[apy]


@pytest.mark.parametrize('wallet_address', [TEST_WALLET_ADDRESS, UNUSED_ADDRESS])
def test_get_staked(wallet_address):
    expected = {TEST_WALLET_ADDRESS: 103.6303835433784, UNUSED_ADDRESS: 0.0}[wallet_address]

    data = Agave.get_staked(wallet_address, block=TEST_BLOCK, blockchain=XDAI, web3=WEB3)
    assert data == [[STK_AGAVE, expected]]
