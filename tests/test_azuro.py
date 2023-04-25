from defi_protocols import Azuro
from defi_protocols.constants import XDAI, WXDAI
from defi_protocols.functions import get_node


WALLET_N1 = '0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f'
NFT_ID = 1099511627781

BLOCK = 27532353
NODE = get_node(XDAI, BLOCK)


def test_get_deposit():
    assert Azuro.get_deposit(WALLET_N1, NFT_ID, Azuro.POOL_ADDR_V2, BLOCK, XDAI, NODE) == 500000000000000000000000


def test_underlying():
    assert Azuro.underlying(WALLET_N1, NFT_ID, BLOCK, XDAI, NODE, rewards=True) == [[WXDAI, 522206.9771458292],
                                                                                    [WXDAI, 22206.97714582918]]


def test_underlying_all():
    assert [[[WXDAI, 2327299.1842438867], [WXDAI, 27299.184243886655]],
            [[WXDAI, 0.0], [WXDAI, 0.028837093647137876]],
            [[WXDAI, 1434603.3214181093], [WXDAI, 4613.321418109328]],
            [[WXDAI, 71451.43632115095], [WXDAI, 1611.490569207598]],
            [[WXDAI, 2327299.1842438867], [WXDAI, 27299.184243886655]]] == Azuro.underlying_all(WALLET_N1,
                                                                                                BLOCK,
                                                                                                XDAI,
                                                                                                NODE,
                                                                                                rewards=True)
