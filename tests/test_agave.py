from defi_protocols import Agave
from defi_protocols.constants import XDAI
from defi_protocols.functions import get_node

STK_AGAVE = '0x610525b415c1BFAeAB1a3fc3d85D87b92f048221'
UNUSED_ADDRESS = '0xc4d46395c01aa86389d4216c2830167878d7cab8'

def test_get_staking_balance():
    web3 = get_node(XDAI)
    data = Agave.get_staking_balance(UNUSED_ADDRESS,block=27038905,blockchain=XDAI,web3=web3)
    assert data == [STK_AGAVE, 103.6303835433784]