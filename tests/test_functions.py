import datetime
import pytz
from pytest import raises
from defi_protocols.functions import get_web3_provider, get_node, get_decimals, get_symbol, date_to_block
from defi_protocols.constants import ETHEREUM, CVX_ETH, ETHTokenAddr, XDAI


def test_get_node():
    node = get_node(ETHEREUM)
    assert node

def test_date_to_block():
    block = 16671547
    assert date_to_block('2023-02-20 18:30:00', ETHEREUM) == block
    date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0)
    assert date_to_block(date, ETHEREUM) == block
    date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0, tzinfo=pytz.UTC)
    assert date_to_block(date, ETHEREUM) == block

def test_get_node_of_unknown_network():
    raises(ValueError, get_node, 'unknown_network')

def test_get_symbol():
    symbol = get_symbol(ETHTokenAddr.DAI, blockchain=ETHEREUM, block=17380523)
    assert symbol == 'DAI'

    symbol = get_symbol("0x0000000000000000000000000000000000000000", blockchain=ETHEREUM, block=17380523)
    assert symbol == 'ETH'

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=ETHEREUM, block=17380523)
    assert symbol == 'ETH'

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=XDAI, block=17380523)
    assert symbol == 'XDAI'
