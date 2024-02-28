"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import DepositPool, StakingPoolManagerEthx, StakingPoolManagerMaticx

# Optionally
class DepositPool(DepositPool):
    ...
"""
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class DepositPool:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "deposit_pool.json"))

    @property
    def burner_role(self) -> bytes:
        return self.contract.functions.BURNER_ROLE().call(block_identifier=self.block)

    @property
    def default_admin_role(self) -> bytes:
        return self.contract.functions.DEFAULT_ADMIN_ROLE().call(block_identifier=self.block)

    @property
    def minter_role(self) -> bytes:
        return self.contract.functions.MINTER_ROLE().call(block_identifier=self.block)

    def allowance(self, owner: str, spender: str) -> int:
        return self.contract.functions.allowance(owner, spender).call(block_identifier=self.block)

    def balance_of(self, account: str) -> int:
        return self.contract.functions.balanceOf(account).call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return self.contract.functions.decimals().call(block_identifier=self.block)

    def get_role_admin(self, role: bytes) -> bytes:
        return self.contract.functions.getRoleAdmin(role).call(block_identifier=self.block)

    def has_role(self, role: bytes, account: str) -> bool:
        return self.contract.functions.hasRole(role, account).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return self.contract.functions.name().call(block_identifier=self.block)

    @property
    def paused(self) -> bool:
        return self.contract.functions.paused().call(block_identifier=self.block)

    @property
    def stader_config(self) -> str:
        return self.contract.functions.staderConfig().call(block_identifier=self.block)

    def supports_interface(self, interface_id: bytes) -> bool:
        return self.contract.functions.supportsInterface(interface_id).call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return self.contract.functions.symbol().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)


class StakingPoolManagerEthx:
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
        self.contract = node.eth.contract(
            address=self.address, abi=load_abi(__file__, "staking_pool_manager_ethx.json")
        )

    @property
    def default_admin_role(self) -> bytes:
        return self.contract.functions.DEFAULT_ADMIN_ROLE().call(block_identifier=self.block)

    def convert_to_assets(self, _shares: int) -> int:
        return self.contract.functions.convertToAssets(_shares).call(block_identifier=self.block)

    def convert_to_shares(self, _assets: int) -> int:
        return self.contract.functions.convertToShares(_assets).call(block_identifier=self.block)

    def deposit(self, _receiver: str, _referral_id: str) -> int:
        """
        Output: _shares
        """
        return self.contract.functions.deposit(_receiver, _referral_id).call(block_identifier=self.block)

    def deposit_1(self, _receiver: str) -> int:
        return self.contract.functions.deposit(_receiver).call(block_identifier=self.block)

    @property
    def excess_eth_deposit_cool_down(self) -> int:
        return self.contract.functions.excessETHDepositCoolDown().call(block_identifier=self.block)

    @property
    def get_exchange_rate(self) -> int:
        return self.contract.functions.getExchangeRate().call(block_identifier=self.block)

    def get_role_admin(self, role: bytes) -> bytes:
        return self.contract.functions.getRoleAdmin(role).call(block_identifier=self.block)

    def has_role(self, role: bytes, account: str) -> bool:
        return self.contract.functions.hasRole(role, account).call(block_identifier=self.block)

    @property
    def is_vault_healthy(self) -> bool:
        return self.contract.functions.isVaultHealthy().call(block_identifier=self.block)

    @property
    def last_excess_eth_deposit_block(self) -> int:
        return self.contract.functions.lastExcessETHDepositBlock().call(block_identifier=self.block)

    @property
    def max_deposit(self) -> int:
        return self.contract.functions.maxDeposit().call(block_identifier=self.block)

    @property
    def min_deposit(self) -> int:
        return self.contract.functions.minDeposit().call(block_identifier=self.block)

    @property
    def paused(self) -> bool:
        return self.contract.functions.paused().call(block_identifier=self.block)

    def preview_deposit(self, _assets: int) -> int:
        return self.contract.functions.previewDeposit(_assets).call(block_identifier=self.block)

    def preview_withdraw(self, _shares: int) -> int:
        return self.contract.functions.previewWithdraw(_shares).call(block_identifier=self.block)

    @property
    def receive_eth_from_auction(self):
        return self.contract.functions.receiveEthFromAuction().call(block_identifier=self.block)

    def receive_excess_eth_from_pool(self, _pool_id: int):
        return self.contract.functions.receiveExcessEthFromPool(_pool_id).call(block_identifier=self.block)

    @property
    def receive_execution_layer_rewards(self):
        return self.contract.functions.receiveExecutionLayerRewards().call(block_identifier=self.block)

    @property
    def receive_withdraw_vault_user_share(self):
        return self.contract.functions.receiveWithdrawVaultUserShare().call(block_identifier=self.block)

    @property
    def stader_config(self) -> str:
        return self.contract.functions.staderConfig().call(block_identifier=self.block)

    def supports_interface(self, interface_id: bytes) -> bool:
        return self.contract.functions.supportsInterface(interface_id).call(block_identifier=self.block)

    @property
    def total_assets(self) -> int:
        return self.contract.functions.totalAssets().call(block_identifier=self.block)


class StakingPoolManagerMaticx:
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
        self.contract = node.eth.contract(
            address=self.address, abi=load_abi(__file__, "staking_pool_manager_maticx.json")
        )

    @property
    def default_admin_role(self) -> bytes:
        return self.contract.functions.DEFAULT_ADMIN_ROLE().call(block_identifier=self.block)

    @property
    def instant_pool_owner(self) -> bytes:
        return self.contract.functions.INSTANT_POOL_OWNER().call(block_identifier=self.block)

    @property
    def claimed_matic(self) -> int:
        return self.contract.functions.claimedMatic().call(block_identifier=self.block)

    def convert_matic_to_matic_x(self, _balance: int) -> tuple[int, int, int]:
        return self.contract.functions.convertMaticToMaticX(_balance).call(block_identifier=self.block)

    def convert_matic_x_to_matic(self, _balance: int) -> tuple[int, int, int]:
        return self.contract.functions.convertMaticXToMatic(_balance).call(block_identifier=self.block)

    def get_amount_after_instant_withdrawal_fees(self, _amount: int) -> tuple[int, int]:
        return self.contract.functions.getAmountAfterInstantWithdrawalFees(_amount).call(block_identifier=self.block)

    @property
    def get_contracts(self) -> tuple[str, str, str]:
        """
        Output: _fxStateChildTunnel, _maticX, _trustedForwarder
        """
        return self.contract.functions.getContracts().call(block_identifier=self.block)

    @property
    def get_matic_x_swap_lock_period(self) -> int:
        return self.contract.functions.getMaticXSwapLockPeriod().call(block_identifier=self.block)

    def get_role_admin(self, role: bytes) -> bytes:
        return self.contract.functions.getRoleAdmin(role).call(block_identifier=self.block)

    def get_user_matic_x_swap_requests(self, _address: str) -> list[tuple]:
        return self.contract.functions.getUserMaticXSwapRequests(_address).call(block_identifier=self.block)

    def has_role(self, role: bytes, account: str) -> bool:
        return self.contract.functions.hasRole(role, account).call(block_identifier=self.block)

    @property
    def instant_pool_matic(self) -> int:
        return self.contract.functions.instantPoolMatic().call(block_identifier=self.block)

    @property
    def instant_pool_matic_x(self) -> int:
        return self.contract.functions.instantPoolMaticX().call(block_identifier=self.block)

    @property
    def instant_pool_owner_1(self) -> str:
        return self.contract.functions.instantPoolOwner().call(block_identifier=self.block)

    @property
    def instant_withdrawal_fee_bps(self) -> int:
        return self.contract.functions.instantWithdrawalFeeBps().call(block_identifier=self.block)

    @property
    def instant_withdrawal_fees(self) -> int:
        return self.contract.functions.instantWithdrawalFees().call(block_identifier=self.block)

    def is_trusted_forwarder(self, _address: str) -> bool:
        return self.contract.functions.isTrustedForwarder(_address).call(block_identifier=self.block)

    @property
    def matic_x_swap_lock_period(self) -> int:
        return self.contract.functions.maticXSwapLockPeriod().call(block_identifier=self.block)

    @property
    def paused(self) -> bool:
        return self.contract.functions.paused().call(block_identifier=self.block)

    @property
    def provide_instant_pool_matic(self):
        return self.contract.functions.provideInstantPoolMatic().call(block_identifier=self.block)

    def supports_interface(self, interface_id: bytes) -> bool:
        return self.contract.functions.supportsInterface(interface_id).call(block_identifier=self.block)

    @property
    def swap_matic_for_matic_x_via_instant_pool(self):
        return self.contract.functions.swapMaticForMaticXViaInstantPool().call(block_identifier=self.block)

    @property
    def treasury(self) -> str:
        return self.contract.functions.treasury().call(block_identifier=self.block)

    @property
    def version(self) -> str:
        return self.contract.functions.version().call(block_identifier=self.block)
