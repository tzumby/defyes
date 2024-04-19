"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import Erc20

# Optionally
class Erc20(Erc20):
    ...
"""

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class Erc20:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "erc20.json"))

    @property
    def name(self) -> str:
        return const_call(self.contract.functions.name())

    @property
    def symbol(self) -> str:
        return const_call(self.contract.functions.symbol())

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    def balance_of(self, arg0: str) -> int:
        return self.contract.functions.balanceOf(arg0).call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)
