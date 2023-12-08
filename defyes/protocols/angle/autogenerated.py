"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import Oracle, Treasury, VaultManager

# Optionally
class Oracle(Oracle):
    ...
"""
from web3 import Web3

from karpatkit.cache import const_call
from defyes.generator import load_abi
from defyes.node import get_node


class Oracle:
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
        node = get_node(blockchain, block)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "oracle.json"))

    @property
    def description(self) -> str:
        return const_call(self.contract.functions.DESCRIPTION())

    @property
    def read(self) -> int:
        return self.contract.functions.read().call(block_identifier=self.block)


class Treasury:
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
        node = get_node(blockchain, block)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "treasury.json"))

    @property
    def stablecoin(self) -> str:
        return const_call(self.contract.functions.stablecoin())

    def vault_manager_list(self, arg0: int) -> str:
        return self.contract.functions.vaultManagerList(arg0).call(block_identifier=self.block)

    def is_vault_manager(self, _vault_manager: str) -> bool:
        return self.contract.functions.isVaultManager(_vault_manager).call(block_identifier=self.block)


class VaultManager:
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
        node = get_node(blockchain, block)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "vault_manager.json"))

    def balance_of(self, owner: str) -> int:
        return self.contract.functions.balanceOf(owner).call(block_identifier=self.block)

    @property
    def vault_id_count(self) -> int:
        return self.contract.functions.vaultIDCount().call(block_identifier=self.block)

    def owner_of(self, vault_id: int) -> str:
        return self.contract.functions.ownerOf(vault_id).call(block_identifier=self.block)

    @property
    def oracle(self) -> str:
        return const_call(self.contract.functions.oracle())

    @property
    def collateral_factor(self) -> int:
        return self.contract.functions.collateralFactor().call(block_identifier=self.block)

    @property
    def base_interest(self) -> int:
        return const_call(self.contract.functions.BASE_INTEREST())

    @property
    def base_params(self) -> int:
        return const_call(self.contract.functions.BASE_PARAMS())

    @property
    def collateral(self) -> str:
        return const_call(self.contract.functions.collateral())

    def get_vault_debt(self, vault_id: int) -> int:
        return self.contract.functions.getVaultDebt(vault_id).call(block_identifier=self.block)

    def vault_data(self, arg0: int) -> tuple[int, int]:
        """
        Output: collateralAmount, normalizedDebt
        """
        return self.contract.functions.vaultData(arg0).call(block_identifier=self.block)

    @property
    def stablecoin(self) -> str:
        return const_call(self.contract.functions.stablecoin())

    @property
    def interest_rate(self) -> int:
        return self.contract.functions.interestRate().call(block_identifier=self.block)
