from decimal import Decimal

from web3 import Web3

from defi_protocols.cache import const_call
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_contract, get_node

# ETH/USD Price Feed
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

# ChainLink Price Feed ABI - latestAnswer, decimals
ABI_CHAINLINK_PRICE_FEED = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'


def get_native_token_price(web3, block, blockchain, decimals=False):
    assert blockchain == ETHEREUM
    price_feed_address = CHAINLINK_ETH_USD

    price_feed_contract = get_contract(
        price_feed_address, blockchain, web3=web3, abi=ABI_CHAINLINK_PRICE_FEED, block=block
    )
    price_feed_decimals = const_call(price_feed_contract.functions.decimals())
    if decimals:
        price_feed_decimals = Decimal(price_feed_decimals)
    native_token_price = price_feed_contract.functions.latestAnswer().call(block_identifier=block) / (
        10**price_feed_decimals
    )

    return native_token_price
