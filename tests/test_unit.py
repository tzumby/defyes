from defi_protocols import Unit
from defi_protocols.constants import ETHEREUM, DAI_ETH
from defi_protocols.functions import get_node

USDP = '0x1456688345527bE1f37E9e627DA0837D6f08C925'
WOOFY = '0x4E15361FD6b4BB609Fa63C81A2be19d873717870'

TEST_BLOCK = 17225800
TEST_WALLET = '0x8442e4FCbbA519B4f4C1EA1FcE57a5379C55906C'
COLLATERAL_ADDRESS = WOOFY
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)


def test_get_cdp_viewer_data():
    x = Unit.get_cdp_viewer_data(TEST_WALLET, COLLATERAL_ADDRESS, TEST_BLOCK, ETHEREUM, WEB3, True)
    assert x == {'icr': 69,
                 'liquidation_ratio': 70,
                 'collateral_address': WOOFY,
                 'collateral_amount': 1.0,
                 'debt_amount': 1.6200187482697077,
                 'liquidation_price': 2.314312497528154,
                 'collateral_usd_value': 0.363742137,
                 'utilization_ratio': 445.3756063652608}


def test_get_cdp_data():
    x = Unit.get_cdp_data(TEST_WALLET, COLLATERAL_ADDRESS, TEST_BLOCK, ETHEREUM, WEB3, True)
    assert x == {'icr': 69,
                 'liquidation_ratio': 70,
                 'stability_fee': 0.9,
                 'liquidation_fee': 5,
                 'issuance_fee': 0.3,
                 'collateral_address': WOOFY,
                 'collateral_amount': 1.0,
                 'debt_address': USDP,
                 'debt_amount': 1.6200187482697077, 
                 'liquidation_price': 2.314312497528154,
                 'collateral_usd_value': 0.363742137,
                 'utilization_ratio': 445.3756063652608,
                 'utilization': 645.4718932829868,
                 'debt_limit': 0.0,
                 'borrowable_debt': -1.6209693836535723}


def test_underlying():
    x = Unit.underlying(TEST_WALLET, TEST_BLOCK, ETHEREUM, WEB3, True)
    assert x == [[[WOOFY, 1.0],
                  [USDP, -1.6200187482697077]],
                 [['0xD0660cD418a64a1d44E9214ad8e459324D8157f1', 559.232649388782],
                  [USDP, -8.724323954416269]],
                 [['0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272', 0.3],
                  [USDP, -1.3048494469519778]],
                 [['0x4bfB2FA13097E5312B19585042FdbF3562dC8676', 2.4],
                  [USDP, -1.6603861686697416]],
                 [['0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1', 0.000642818733893975],
                  [USDP, -3.8895164230934722]],
                 [['0xdB25f211AB05b1c97D595516F45794528a807ad8', 4.0],
                  [USDP, -2.0642833598427193]],
                 [['0xcE5147182624fD121d0CE974847A8DbFCa9358B7', 7.60053991711e-07],
                  [USDP, -19.645142679366515]],
                 [['0x0770E27F92F0D0e716dc531037B8b87FEFEbE561', 1.0],
                  [USDP, -1.0]]]

