import logging
from dataclasses import dataclass
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import balance_of, to_token_amount

logger = logging.getLogger(__name__)


@dataclass
class EthDerivative:
    protocol: str
    description: str
    addr: str
    blockchain: str
    underlying_token: str
    eth_value_function: str
    eth_value_abi: str

    def underlying(self, wallet: str, block: int | str, decimals: bool, web3: Web3) -> Decimal:
        wallet = web3.to_checksum_address(wallet)
        contract = web3.eth.contract(address=self.addr, abi=self.eth_value_abi)
        amount = balance_of(wallet, self.addr, block, self.blockchain, decimals=False)
        eth_value = contract.functions[self.eth_value_function](int(amount)).call(block_identifier=block)
        return to_token_amount(self.underlying_token, amount=eth_value, blockchain=self.blockchain, web3=web3, decimals=decimals)
