
from defi_protocols import Maker
from defi_protocols.functions import get_node
from defi_protocols.constants import ETHEREUM, DAI_ETH, WETH_ETH, ETHTokenAddr


TEST_BLOCK = 17070386
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)
# TEST_WALLET = '0xf929122994e177079c924631ba13fb280f5cd1f9'
# TEST_WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
TEST_WALLET = '0x4971DD016127F390a3EF6b956Ff944d0E2e1e462'
VAULT_ID = 27353


def test_get_vault_data():
    x = Maker.get_vault_data(VAULT_ID, TEST_BLOCK, WEB3)
    assert x == {'mat': 1.6,
                 'gem': ETHTokenAddr.stETH,
                 'dai': DAI_ETH, 
                 'ink': 57328.918780519,
                 'art': 21811755.174275193,
                 'Art': 131281671.56044462,
                 'rate': 1.0337823922958922,
                 'spot': 1456.9286150664384,
                 'line': 154522941.83599702,
                 'dust': 7500.0}


def test_underlying():
    x = Maker.underlying(VAULT_ID, TEST_BLOCK, WEB3)
    assert x == [[ETHTokenAddr.stETH, 57328.918780519],
                 [DAI_ETH, -22548608.444234513]]

def test_get_delegated_MKR():
    x = Maker.get_delegated_MKR(TEST_WALLET, TEST_BLOCK, WEB3,
                                decimals=False)
    assert x == [[ETHTokenAddr.MKR, 583805204609736124092]]
