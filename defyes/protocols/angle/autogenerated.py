"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import Oracle, Treasury, VaultManager, Steur

# Optionally
class Oracle(Oracle):
    ...
"""
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


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
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "oracle.json"))

    @property
    def description(self) -> str:
        return const_call(self.contract.functions.DESCRIPTION())

    @property
    def read(self) -> int:
        """
        Output: quoteAmount
        """
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
        node = get_node(blockchain)
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
        node = get_node(blockchain)
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


class Steur:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "steur.json"))

    @property
    def access_control_manager(self) -> str:
        return self.contract.functions.accessControlManager().call(block_identifier=self.block)

    def allowance(self, owner: str, spender: str) -> int:
        return self.contract.functions.allowance(owner, spender).call(block_identifier=self.block)

    @property
    def asset(self) -> str:
        return const_call(self.contract.functions.asset())

    def balance_of(self, account: str) -> int:
        return self.contract.functions.balanceOf(account).call(block_identifier=self.block)

    def compute_updated_assets(self, _total_assets: int, exp: int) -> int:
        return self.contract.functions.computeUpdatedAssets(_total_assets, exp).call(block_identifier=self.block)

    def convert_to_assets(self, shares: int) -> int:
        """
        Output: assets
        """
        return self.contract.functions.convertToAssets(shares).call(block_identifier=self.block)

    def convert_to_shares(self, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.convertToShares(assets).call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    @property
    def estimated_apr(self) -> int:
        """
        Output: apr
        """
        return self.contract.functions.estimatedAPR().call(block_identifier=self.block)

    def is_governor(self, admin: str) -> bool:
        return self.contract.functions.isGovernor(admin).call(block_identifier=self.block)

    def is_governor_or_guardian(self, admin: str) -> bool:
        return self.contract.functions.isGovernorOrGuardian(admin).call(block_identifier=self.block)

    @property
    def last_update(self) -> int:
        return self.contract.functions.lastUpdate().call(block_identifier=self.block)

    def max_deposit(self, arg0: str) -> int:
        return self.contract.functions.maxDeposit(arg0).call(block_identifier=self.block)

    def max_mint(self, arg0: str) -> int:
        return self.contract.functions.maxMint(arg0).call(block_identifier=self.block)

    @property
    def max_rate(self) -> int:
        return self.contract.functions.maxRate().call(block_identifier=self.block)

    def max_redeem(self, owner: str) -> int:
        return self.contract.functions.maxRedeem(owner).call(block_identifier=self.block)

    def max_withdraw(self, owner: str) -> int:
        return self.contract.functions.maxWithdraw(owner).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return self.contract.functions.name().call(block_identifier=self.block)

    @property
    def paused(self) -> int:
        return self.contract.functions.paused().call(block_identifier=self.block)

    def preview_deposit(self, assets: int) -> int:
        return self.contract.functions.previewDeposit(assets).call(block_identifier=self.block)

    def preview_mint(self, shares: int) -> int:
        return self.contract.functions.previewMint(shares).call(block_identifier=self.block)

    def preview_redeem(self, shares: int) -> int:
        return self.contract.functions.previewRedeem(shares).call(block_identifier=self.block)

    def preview_withdraw(self, assets: int) -> int:
        return self.contract.functions.previewWithdraw(assets).call(block_identifier=self.block)

    @property
    def rate(self) -> int:
        return self.contract.functions.rate().call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return const_call(self.contract.functions.symbol())

    @property
    def total_assets(self) -> int:
        return self.contract.functions.totalAssets().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)
