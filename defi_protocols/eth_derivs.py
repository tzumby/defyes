import logging
from dataclasses import dataclass
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import balance_of, to_token_amount, get_decimals

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

    def unwrap(self, amount: Decimal | int | float, block: int | str, web3: Web3) -> Decimal:
        contract = web3.eth.contract(address=self.addr, abi=self.eth_value_abi)
        token_decimals = get_decimals(self.addr, blockchain=self.blockchain, web3=web3)
        amount = int(Decimal(amount)*Decimal(10**token_decimals))
        eth_value = contract.functions[self.eth_value_function](amount).call(block_identifier=block)
        eth_value = Decimal(eth_value)/Decimal(10**token_decimals)
        return to_token_amount(self.addr, amount=eth_value, blockchain=self.blockchain, web3=web3, decimals=True)

    def underlying(self, wallet: str, block: int | str, decimals: bool, web3: Web3, unwrapped: bool=True) -> Decimal:
        wallet = web3.to_checksum_address(wallet)
        contract = web3.eth.contract(address=self.addr, abi=self.eth_value_abi)
        amount = balance_of(wallet, self.addr, block, self.blockchain, decimals=False)
        if unwrapped:
            return self.unwrap(amount, block, web3)
        else:
            return to_token_amount(self.addr, amount=amount, blockchain=self.blockchain, web3=web3, decimals=decimals)

