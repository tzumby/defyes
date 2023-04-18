
from defi_protocols import Maker
from defi_protocols.functions import get_node
from defi_protocols.constants import ETHEREUM, DAI_ETH, WETH_ETH, ETHTokenAddr


TEST_BLOCK = 17070386
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)
# TEST_WALLET = '0xf929122994e177079c924631ba13fb280f5cd1f9'
TEST_WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
VAULT_ID = 10


def test_get_vault_data():
    x = Maker.get_vault_data(VAULT_ID, TEST_BLOCK, WEB3, 1, 1)
    assert x == {'mat': 1.45,
                 'gem': WETH_ETH,
                 'dai': DAI_ETH, 
                 'ink': 0.0,
                 'art': 0.0,
                 'Art': 213059126.61267862,
                 'rate': 1.0877561923001058,
                 'spot': 1434.1094163,
                 'line': 421276896.85485435,
                 'dust': 7500.0}


def test_underlying():
    x = Maker.underlying(VAULT_ID, TEST_BLOCK, WEB3, 1, 1)
    assert x == [[WETH_ETH, 0.0],
                 [DAI_ETH, 0.0]]


def test_get_delegated_MKR():
    x = Maker.get_delegated_MKR(TEST_WALLET, TEST_BLOCK, WEB3,
                                decimals=False, index=1, execution=1)
    assert x == [[ETHTokenAddr.MKR, 0]]
