import logging

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


def test_get_staking_balance():
    data = Agave.get_staked(TEST_WALLET_ADDRESS, block=TEST_BLOCK, blockchain=XDAI, web3=WEB3)
    assert data == [[STK_AGAVE, 103.6303835433784]]

    data = Agave.get_staked(UNUSED_ADDRESS, block=TEST_BLOCK, blockchain=XDAI, web3=WEB3)
    assert data == [[STK_AGAVE, 0.0]]
