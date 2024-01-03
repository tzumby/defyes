"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import BaseVault

# Optionally
class BaseVault(BaseVault):
    ...
"""
from web3 import Web3

from karpatkit.cache import const_call
from defyes.generator import load_abi
from defyes.node import get_node


class BaseVault:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "base_vault.json"))

    @property
    def denominator(self) -> int:
        return self.contract.functions.DENOMINATOR().call(block_identifier=self.block)

    @property
    def domain_separator(self) -> bytes:
        return self.contract.functions.DOMAIN_SEPARATOR().call(block_identifier=self.block)

    @property
    def investor_ratio(self) -> int:
        return self.contract.functions.INVESTOR_RATIO().call(block_identifier=self.block)

    @property
    def max_withdraw_fee(self) -> int:
        return self.contract.functions.MAX_WITHDRAW_FEE().call(block_identifier=self.block)

    @property
    def min_initial_assets(self) -> int:
        return self.contract.functions.MIN_INITIAL_ASSETS().call(block_identifier=self.block)

    def allowance(self, owner: str, spender: str) -> int:
        return self.contract.functions.allowance(owner, spender).call(block_identifier=self.block)

    def approve(self, spender: str, amount: int) -> bool:
        return self.contract.functions.approve(spender, amount).call(block_identifier=self.block)

    @property
    def asset(self) -> str:
        return self.contract.functions.asset().call(block_identifier=self.block)

    def assets_of(self, owner: str) -> int:
        return self.contract.functions.assetsOf(owner).call(block_identifier=self.block)

    @property
    def available_cap(self) -> int:
        return self.contract.functions.availableCap().call(block_identifier=self.block)

    def balance_of(self, account: str) -> int:
        return self.contract.functions.balanceOf(account).call(block_identifier=self.block)

    @property
    def configuration(self) -> str:
        return self.contract.functions.configuration().call(block_identifier=self.block)

    @property
    def controller(self) -> str:
        return self.contract.functions.controller().call(block_identifier=self.block)

    def convert_to_assets(self, shares: int) -> int:
        return self.contract.functions.convertToAssets(shares).call(block_identifier=self.block)

    def convert_to_shares(self, assets: int) -> int:
        return self.contract.functions.convertToShares(assets).call(block_identifier=self.block)

    @property
    def current_round_id(self) -> int:
        return self.contract.functions.currentRoundId().call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    def decrease_allowance(self, spender: str, subtracted_value: int) -> bool:
        return self.contract.functions.decreaseAllowance(spender, subtracted_value).call(block_identifier=self.block)

    @property
    def deposit_queue_size(self) -> int:
        return self.contract.functions.depositQueueSize().call(block_identifier=self.block)

    @property
    def get_withdraw_fee_ratio(self) -> int:
        return self.contract.functions.getWithdrawFeeRatio().call(block_identifier=self.block)

    def idle_assets_of(self, owner: str) -> int:
        return self.contract.functions.idleAssetsOf(owner).call(block_identifier=self.block)

    def increase_allowance(self, spender: str, added_value: int) -> bool:
        return self.contract.functions.increaseAllowance(spender, added_value).call(block_identifier=self.block)

    @property
    def investor(self) -> str:
        return self.contract.functions.investor().call(block_identifier=self.block)

    @property
    def is_processing_deposits(self) -> bool:
        return self.contract.functions.isProcessingDeposits().call(block_identifier=self.block)

    @property
    def last_round_assets(self) -> int:
        return self.contract.functions.lastRoundAssets().call(block_identifier=self.block)

    @property
    def last_share_price(self) -> tuple[int, int]:
        """
        Output: numerator, denominator
        """
        return self.contract.functions.lastSharePrice().call(block_identifier=self.block)

    def max_deposit(self, arg0: str) -> int:
        return self.contract.functions.maxDeposit(arg0).call(block_identifier=self.block)

    def max_mint(self, arg0: str) -> int:
        return self.contract.functions.maxMint(arg0).call(block_identifier=self.block)

    def max_redeem(self, owner: str) -> int:
        return self.contract.functions.maxRedeem(owner).call(block_identifier=self.block)

    def max_withdraw(self, owner: str) -> int:
        return self.contract.functions.maxWithdraw(owner).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return const_call(self.contract.functions.name())

    def nonces(self, owner: str) -> int:
        return self.contract.functions.nonces(owner).call(block_identifier=self.block)

    def permit(self, owner: str, spender: str, value: int, deadline: int, v: int, r: bytes, s: bytes):
        return self.contract.functions.permit(owner, spender, value, deadline, v, r, s).call(
            block_identifier=self.block
        )

    def preview_deposit(self, assets: int) -> int:
        return self.contract.functions.previewDeposit(assets).call(block_identifier=self.block)

    def preview_mint(self, shares: int) -> int:
        return self.contract.functions.previewMint(shares).call(block_identifier=self.block)

    def preview_redeem(self, shares: int) -> int:
        return self.contract.functions.previewRedeem(shares).call(block_identifier=self.block)

    def preview_withdraw(self, assets: int) -> int:
        return self.contract.functions.previewWithdraw(assets).call(block_identifier=self.block)

    @property
    def processed_deposits(self) -> int:
        return self.contract.functions.processedDeposits().call(block_identifier=self.block)

    @property
    def queued_deposits(self) -> list[str]:
        return self.contract.functions.queuedDeposits().call(block_identifier=self.block)

    @property
    def share_price(self) -> int:
        return self.contract.functions.sharePrice().call(block_identifier=self.block)

    @property
    def share_price_decimals(self) -> int:
        return self.contract.functions.sharePriceDecimals().call(block_identifier=self.block)

    @property
    def spent_cap(self) -> int:
        return self.contract.functions.spentCap().call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return const_call(self.contract.functions.symbol())

    @property
    def total_assets(self) -> int:
        return self.contract.functions.totalAssets().call(block_identifier=self.block)

    @property
    def total_idle_assets(self) -> int:
        return self.contract.functions.totalIdleAssets().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)

    def transfer(self, to: str, amount: int) -> bool:
        return self.contract.functions.transfer(to, amount).call(block_identifier=self.block)

    def transfer_from(self, from_: str, to: str, amount: int) -> bool:
        return self.contract.functions.transferFrom(from_, to, amount).call(block_identifier=self.block)
