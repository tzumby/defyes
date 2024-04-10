"""This module contains the functions to interact with the mu protocol.
The main function is `get_protocol_data_for` that returns the data for a wallet for mu exchange.
for more info on the mu exchange protocol, see https://docs.mu.exchange/staking/usdmsdai-vault.
"""

from web3 import Web3

from defyes.functions import ensure_a_block_number
from defyes.protocols.maker import reduce_sdai
from defyes.protocols.mu.autogenerated import TradingVault
from defyes.types import Addr, Token, TokenAmount


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    lptoken_address: str,
    block: int | str = "latest",
) -> dict:
    """Get the data for a wallet for mu exchange. Currently there's just one vault that is supported.
    msDAI vault is the only one."""
    wallet = Addr(Web3.to_checksum_address(wallet))
    lptoken_address = Web3.to_checksum_address(lptoken_address)
    block_id = ensure_a_block_number(block, blockchain)

    # Get the trading vault with the msDAI balance info
    tv = TradingVault(blockchain, block_id, lptoken_address)

    # Get the amount of the holdings we have
    holdings_amount = TokenAmount.from_teu(tv.balance_of(wallet), Token(lptoken_address, blockchain))
    # Reduce sDAI to the elementary token DAI and
    address, amount = reduce_sdai(tv.standard_token, int(holdings_amount.balance()), block_id, blockchain)
    amount = TokenAmount.from_teu(amount, Token(address, blockchain)).balance(True)

    position_data = [{"address": lptoken_address, "balance": holdings_amount.balance(True)}]
    underlying_data = [{"address": address, "balance": amount}]

    data = {
        "blockchain": blockchain,
        "block_id": block_id,
        "protocol": "Mu Exchange",
        "positions_key": "holding_token_address",
        "version": 0,
        "wallet": wallet,
        "decimals": tv.decimals,
        "positions": {
            lptoken_address: {
                "holdings": position_data,
                "underlyings": underlying_data,
            }
        },
    }

    return data
