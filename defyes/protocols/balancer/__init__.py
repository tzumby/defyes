from contextlib import suppress
from datetime import datetime, timedelta
from decimal import Decimal
from functools import cached_property

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.constants import Address, Chain
from defyes.functions import block_to_date, date_to_block, get_logs_web3, last_block, to_token_amount
from defyes.helpers import suppress_error_codes
from defyes.node import get_node
from defyes.prices.prices import get_price

from .autogenerated import (
    Gauge,
    GaugeFactory,
    GaugeRewardHelper,
    LiquidityPool,
    PoolToken,
    Vault,
    Vebal,
    VebalFeeDistributor,
)

# First block in every blockchain
START_BLOCK = {
    "ethereumv1": 14457664,
    Chain.ETHEREUM: 15399251,
    Chain.POLYGON: 40687417,
    Chain.ARBITRUM: 72942741,
    Chain.GNOSIS: 27088528,
}


class Vault(Vault):
    ADDR: str = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: ADDR,
        Chain.POLYGON: ADDR,
        Chain.GNOSIS: ADDR,
        Chain.ARBITRUM: ADDR,
    }

    def get_pool_data(self, pool_id: int) -> list:
        tokens = []
        pool_data = self.get_pool_tokens(pool_id)
        for token, balance in zip(pool_data[0], pool_data[1]):
            tokens.append((token, balance))

        return tokens


class PoolToken(PoolToken):
    @property
    def rate(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return self.get_rate

    @property
    def underlying(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().underlying

    @property
    def underlying_asset_address(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().underlying_asset_address

    @property
    def steth(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return self.st_eth

    @property
    def is_wsteth(self) -> bool:
        return self.steth is not None

    def get_token_addr_steth(self, scaling_factor) -> str:
        main_token = self.underlying
        if scaling_factor:
            main_token = self.underlying_asset_address
            if main_token is None:
                main_token = self.address
                stETH = self.steth
                if stETH is not None:
                    if scaling_factor != 10**18:
                        main_token = stETH
                    else:
                        main_token = self.address
                else:
                    main_token = self.address

        return main_token

    def get_token_addr_wsteth(self) -> str:
        main_token = self.underlying
        if main_token is None:
            main_token = self.underlying_asset_address
            if main_token is None:
                main_token = self.address

        return main_token

    def calc_amount(self, token_amount: int, decimals: bool = True, scaling_factor: int = None) -> Decimal:
        token_amount = Decimal(token_amount)
        if scaling_factor and not self.is_wsteth:
            # uncomment to have stETH being returned instead of wstETH
            # if scaling_factor:
            token_amount = token_amount * Decimal(scaling_factor) / Decimal(10 ** (2 * 18 - self.decimals))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


class LiquidityPool(LiquidityPool):
    @cached_property
    def poolid(self):
        try:
            return self.get_pool_id
        except ContractLogicError:
            return self.pool_id

    @cached_property
    def bpt_index(self) -> int | None:
        with suppress(ContractLogicError), suppress_error_codes():
            return self.get_bpt_index

    @cached_property
    def supply(self) -> int:
        """
        Return the first valid attribure: get_actual_supply or get_virtual_supply, otherwise total_supply.
        """
        for attr in ("get_actual_supply", "get_virtual_supply"):
            with suppress(ContractLogicError), suppress_error_codes():
                return getattr(self, attr)
        return self.total_supply

    @cached_property
    def scaling_factors(self) -> int | None:
        with suppress(ContractLogicError):
            return self.get_scaling_factors

    def balance_of(self, wallet: str) -> int:
        wallet = Web3.to_checksum_address(wallet)
        return super().balance_of(wallet)

    def swap_fee_percentage_for(self, block: int | str) -> int:
        return self.contract.functions.getSwapFeePercentage().call(block_identifier=block)

    def swap_fees(self, vault_address: str, block_start: int, decimals: bool = True) -> list[dict]:
        node = self.contract.w3
        pool_id = "0x" + self.poolid.hex()
        swap_event = node.keccak(text="Swap(bytes32,address,address,uint256,uint256)").hex()

        if block_start < START_BLOCK[self.blockchain]:
            block_start = START_BLOCK[self.blockchain]

        swap_logs = get_logs_web3(
            address=vault_address,
            blockchain=self.blockchain,
            block_start=block_start,
            block_end=self.block,
            topics=[swap_event, pool_id],
            web3=node,
        )

        swaps = []
        for swap_log in swap_logs:
            token_in = Web3.to_checksum_address(f"0x{swap_log['topics'][2].hex()[-40:]}")
            swap_fee = Decimal(self.swap_fee_percentage_for(swap_log["blockNumber"]))
            swap_fee /= Decimal(10**self.decimals)
            swap_fee *= int(swap_log["data"].hex()[2:66], 16)

            swap_data = {
                "block": swap_log["blockNumber"],
                "token_in": token_in,
                "amount_in": to_token_amount(token_in, swap_fee, self.blockchain, node, decimals),
            }

            swaps.append(swap_data)

        return swaps

    def calc_balance(self, wallet: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


class GaugeFactory(GaugeFactory):
    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: "0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC",
        "ethereum_v2": "0xf1665E19bc105BE4EDD3739F88315cC699cc5b65",
        # 'polygon': '0x3b8cA519122CdD8efb272b0D3085453404B25bD0', # DEPRECATED
        Chain.POLYGON: "0x22625eEDd92c81a219A83e1dc48f88d54786B017",
        # 'arbitrum': '0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2', # DEPRECATED
        Chain.ARBITRUM: "0x6817149cb753BF529565B4D023d7507eD2ff4Bc0",
        # 'xdai': '0x809B79b53F18E9bc08A961ED4678B901aC93213a', # DEPRECATED
        Chain.GNOSIS: "0x83E443EF4f9963C77bd860f94500075556668cb8",
    }

    def __init__(self, blockchain: str, block: int, lp_address: str, address: str | None = None) -> None:
        if isinstance(block, str) and block == "latest" and blockchain == Chain.ETHEREUM:
            block = last_block(Chain.ETHEREUM)
        super().__init__(blockchain, block, address)
        lp_address = Web3.to_checksum_address(lp_address)
        self.address = self._update_address(lp_address)
        self.gauge_address = self._gauge_address(lp_address)

    def _update_address(self, lp_address: str) -> str:
        new_address = self.address
        if self.blockchain == Chain.ETHEREUM:
            if self.get_pool_gauge(lp_address) == Address.ZERO:
                new_address = self.default_addresses["ethereum_v2"]

        return new_address

    def _gauge_address(self, lp_address: str) -> str:
        if self.address == self.default_addresses[Chain.ETHEREUM]:
            gauge_address = self.get_pool_gauge(lp_address)
        else:
            block_from = START_BLOCK[self.blockchain]
            gauge_created_event_signature = "GaugeCreated(address)"
            gauge_created_event = Web3.keccak(text=gauge_created_event_signature).hex()

            gauge_address = Address.ZERO
            if self.block == "latest" or self.block >= block_from:
                logs = get_logs_web3(
                    address=self.address,
                    blockchain=self.blockchain,
                    block_start=block_from,
                    block_end=self.block,
                    topics=[gauge_created_event],
                    web3=self.contract.w3,
                )
                for log in logs:
                    tx = self.contract.w3.eth.get_transaction(log["transactionHash"])
                    if lp_address[2 : len(lp_address)].lower() in tx["input"]:
                        gauge_address = Web3.to_checksum_address(f"0x{log['topics'][1].hex()[-40:]}")
                        break
            else:
                raise ValueError(f"Block {self.block} should be higher than first valid block: {block_from}")

        return gauge_address


class Gauge(Gauge):
    BAL_ADDRS: dict = {
        Chain.ETHEREUM: "0xba100000625a3754423978a60c9317c58a424e3D",
        Chain.POLYGON: "0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3",
        Chain.ARBITRUM: "0x040d1EdC9569d4Bab2D15287Dc5A4F10F56a56B8",
        Chain.GNOSIS: "0x7eF541E2a22058048904fE5744f9c7E4C57AF717",
    }

    @property
    def decimals(self):
        return 18 if self.address == Address.ZERO else super().decimals

    def balance_of(self, wallet: str) -> Decimal:
        wallet = Web3.to_checksum_address(wallet)
        if self.address == Address.ZERO:
            return Decimal(self.contract.w3.eth.get_balance(wallet, self.block))
        else:
            with suppress(ContractLogicError):
                return super().balance_of(wallet)
        return Decimal(0)

    def get_rewards(self, wallet: str, decimals: bool = True) -> dict:
        rewards = {}
        if self.address != Address.ZERO:
            wallet = Web3.to_checksum_address(wallet)

            # BAL rewards
            bal_decimals = Decimal(10**18) if decimals else 1
            rewards = {self.BAL_ADDRS[self.blockchain]: self.claimable_tokens(wallet) / bal_decimals}

            tokens = [self.reward_tokens(n) for n in range(self.reward_count)]
            for token_address in tokens:
                if self.blockchain == Chain.ETHEREUM:
                    token_reward = self.claimable_reward(wallet, token_address)
                else:
                    token_reward = GaugeRewardHelper(self.blockchain, self.block).get_rewards(
                        self.address, wallet, token_address
                    )

                rewards[token_address] = to_token_amount(
                    token_address, token_reward, self.blockchain, self.contract.w3, decimals
                )

        return rewards

    def calc_balance(self, wallet: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


class GaugeRewardHelper(GaugeRewardHelper):
    default_addresses: dict[str, str] = {
        Chain.GNOSIS: "0xf7D5DcE55E6D47852F054697BAB6A1B48A00ddbd",
        Chain.POLYGON: "0xaEb406b0E430BF5Ea2Dc0B9Fe62E4E53f74B3a33",
        Chain.ARBITRUM: "0xA0DAbEBAAd1b243BBb243f933013d560819eB66f",
    }

    def get_rewards(self, gauge_address: str, wallet: str, token_address: str) -> Decimal:
        gauge_address = Web3.to_checksum_address(gauge_address)
        wallet = Web3.to_checksum_address(wallet)
        token_address = Web3.to_checksum_address(token_address)
        return self.get_pending_rewards(gauge_address, wallet, token_address)


class Vebal(Vebal):
    default_addresses: dict[str, str] = {Chain.ETHEREUM: "0xC128a9954e6c874eA3d62ce62B468bA073093F25"}

    def balance_of(self, wallet: str, token_address: str) -> Decimal:
        wallet = Web3.to_checksum_address(wallet)
        if token_address == self.token:
            with suppress(ContractLogicError):
                return Decimal(self.locked(wallet)[0])
        return Decimal(0)

    def calc_balance(self, wallet: str, token_address: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet, token_address))
        if decimals:
            token_amount = token_amount / Decimal(10**18)
        return token_amount


class VebalFeeDistributor(VebalFeeDistributor):
    default_addresses: dict[str, str] = {Chain.ETHEREUM: "0xD3cf852898b21fc233251427c2DC93d3d604F3BB"}

    REWARD_TOKENS: list = [
        "0xba100000625a3754423978a60c9317c58a424e3D",
        "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2",
        "0xA13a9247ea42D743238089903570127DdA72fE44",
    ]

    def get_rewards(self, wallet: str, decimals: bool = True) -> dict:
        rewards = self.claim_tokens(wallet, self.REWARD_TOKENS)
        rewards_decimals = 18 if decimals else 0
        rewards = [Decimal(r) / Decimal(10**rewards_decimals) for r in rewards]
        return dict(zip(self.REWARD_TOKENS, rewards))


def unwrap(blockchain: str, lp_address: str, amount: Decimal, block: int | str, decimals: bool = True) -> None:
    lp = LiquidityPool(blockchain, block, lp_address)
    pool_tokens = Vault(blockchain, block).get_pool_data(lp.poolid)
    pool_balance_fraction = Decimal(amount) * Decimal(10**lp.decimals) / Decimal(lp.supply)

    balances = {}
    for n, (token_addr, balance) in enumerate(pool_tokens):
        if n == lp.bpt_index:
            continue

        token = PoolToken(blockchain, block, token_addr)
        if token.rate is not None:
            for token_addr, token_balance in unwrap(
                blockchain, token.address, token.calc_amount(balance, decimals), block
            ).items():
                balances[token_addr] = balances.get(token_addr, 0) + token_balance * pool_balance_fraction
        else:
            scaling_factor = None if lp.scaling_factors is None else lp.scaling_factors[n]
            token_addr = token.get_token_addr_wsteth()
            token_balance = token.calc_amount(balance, decimals, scaling_factor)

            balances[token_addr] = balances.get(token_addr, 0) + token_balance * pool_balance_fraction
    return balances


def pool_balances(blockchain: str, lp_address: str, block: int | str, decimals: bool = True) -> None:
    lp = LiquidityPool(blockchain, block, lp_address)
    pool_tokens = Vault(blockchain, block).get_pool_data(lp.poolid)

    balances = {}
    for n, (token_addr, balance) in enumerate(pool_tokens):
        if n == lp.bpt_index:
            continue

        token = PoolToken(blockchain, block, token_addr)
        if token.rate is not None:
            for token_addr, token_balance in unwrap(
                blockchain, token.address, token.calc_amount(balance, decimals), block
            ).items():
                balances[token_addr] = balances.get(token_addr, 0) + token_balance
        else:
            scaling_factor = None if lp.scaling_factors is None else lp.scaling_factors[n]
            token_addr = token.get_token_addr_wsteth()
            token_balance = token.calc_amount(balance, decimals, scaling_factor)

            balances[token_addr] = balances.get(token_addr, 0) + token_balance
    return balances


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    lp_addrs: str | list,
    block: int | str = "latest",
    reward: bool = False,
    decimals: bool = True,
    aura_staked: Decimal = None,
) -> None:
    if isinstance(lp_addrs, str):
        lp_addrs = [lp_addrs]

    positions = {}
    for lp_address in lp_addrs:
        positions[lp_address] = {"liquidity": {}, "staked": {}, "locked": {}, "financial_metrics": {}}
        gauge_address = GaugeFactory(blockchain, block, lp_address).gauge_address
        gauge = Gauge(blockchain, block, gauge_address)
        lp = LiquidityPool(blockchain, block, lp_address)

        lp_balance = lp.balance_of(wallet)
        pool_balance_fraction = lp_balance / Decimal(lp.supply)
        if lp_balance:
            positions[lp_address]["liquidity"] = {
                "holdings": [{"address": lp_address, "balance": lp.calc_balance(wallet, decimals)}]
            }

        lp_balance_staked = gauge.balance_of(wallet)
        pool_staked_fraction = lp_balance_staked / Decimal(lp.supply)
        if lp_balance_staked:
            positions[lp_address]["staked"] = {
                "holdings": [{"address": lp_address, "balance": gauge.calc_balance(wallet, decimals)}]
            }

        if blockchain == Chain.ETHEREUM:
            vebal = Vebal(blockchain, block)
            lp_balance_locked = vebal.balance_of(wallet, lp.address)
            pool_locked_fraction = lp_balance_locked / Decimal(lp.supply)
            if lp_balance_locked:
                positions[lp_address]["locked"] = {
                    "holdings": [{"address": lp_address, "balance": vebal.calc_balance(wallet, lp_address, decimals)}]
                }
        else:
            pool_locked_fraction = Decimal(0)

        balances = pool_balances(blockchain, lp_address, block, decimals)
        for addr, amount in balances.items():
            balance = amount * pool_balance_fraction
            if balance:
                positions[lp_address]["liquidity"]["underlyings"] = positions[lp_address]["liquidity"].get(
                    "underlyings", []
                )
                positions[lp_address]["liquidity"]["underlyings"].append({"address": addr, "balance": balance})

            if aura_staked is None:
                balance_staked = amount * pool_staked_fraction
            else:
                aura_pool_fraction = aura_staked / Decimal(lp.supply)
                balance_staked = amount * aura_pool_fraction
            if balance_staked:
                positions[lp_address]["staked"]["underlyings"] = positions[lp_address]["staked"].get("underlyings", [])
                positions[lp_address]["staked"]["underlyings"].append({"address": addr, "balance": balance_staked})

            balance_locked = amount * pool_locked_fraction
            if balance_locked:
                positions[lp_address]["locked"]["underlyings"] = positions[lp_address]["locked"].get("underlyings", [])
                positions[lp_address]["locked"]["underlyings"].append({"address": addr, "balance": balance_locked})

        if reward:
            rewards = gauge.get_rewards(wallet)
            for addr, reward in rewards.items():
                if reward:
                    positions[lp_address]["staked"]["unclaimed_rewards"] = positions[lp_address]["staked"].get(
                        "unclaimed_rewards", []
                    )
                    positions[lp_address]["staked"]["unclaimed_rewards"].append({"address": addr, "balance": reward})

            if blockchain == Chain.ETHEREUM:
                vebal_distributor = VebalFeeDistributor(blockchain, block)
                vebal_rewards = vebal_distributor.get_rewards(wallet)
                for addr, reward in vebal_rewards.items():
                    if reward:
                        positions[lp_address]["locked"]["unclaimed_rewards"] = positions[lp_address]["locked"].get(
                            "unclaimed_rewards", []
                        )
                        positions[lp_address]["locked"]["unclaimed_rewards"].append(
                            {"address": addr, "balance": reward}
                        )

    return {
        "protocol": "Balancer",
        "blockchain": blockchain,
        "block": block,
        "positions": positions,
        "positions_key": "liquidity_pool_address",
        "version": 0,
    }


def get_swap_fees_apr(
    lptoken_address: str, blockchain: str, block: int | str = "latest", days: int = 1, apy: bool = False
) -> Decimal:
    block_start = date_to_block(
        datetime.strftime(
            datetime.strptime(block_to_date(block, blockchain), "%Y-%m-%d %H:%M:%S") - timedelta(days=days),
            "%Y-%m-%d %H:%M:%S",
        ),
        blockchain,
    )

    node = get_node(blockchain, block)
    vault_address = Vault(blockchain, block).address
    lp = LiquidityPool(blockchain, block, lptoken_address)
    swaps = lp.swap_fees(vault_address, block_start)

    # create a dictionary to store the total amountIn for each tokenIn
    totals = {}
    for swap in swaps:
        totals[swap["token_in"]] = totals.get(swap["token_in"], 0) + swap["amount_in"]

    fee = 0
    for token, amount in totals.items():
        fee += amount * Decimal(get_price(token, block, blockchain, node)[0])

    pool_balance = pool_balances(blockchain, lptoken_address, block)
    tvl = 0
    for token, balance in pool_balance.items():
        tvl += balance * Decimal(get_price(token, block, blockchain, node)[0])

    rate = Decimal(fee / tvl)
    apr = (((1 + rate) ** Decimal(365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        return (1 + (apr / seconds_per_year)) ** seconds_per_year - 1
    else:
        return apr
