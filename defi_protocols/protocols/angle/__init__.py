import logging
from decimal import Decimal

from web3 import Web3
from web3.exceptions import ContractCustomError, ContractLogicError

from defi_protocols.cache import cache_contract_method
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_decimals, get_node
from . import abstract

logger = logging.getLogger(__name__)


# Borrow Module
# https://docs.angle.money/angle-borrowing-module/borrowing-module
# https://github.com/AngleProtocol/borrow-contracts/tree/main
class Treasury(abstract.Treasury):
    # https://developers.angle.money/borrowing-module-contracts/smart-contract-docs/treasury
    # https://github.com/AngleProtocol/borrow-contracts/tree/main/contracts/treasury
    ADDRS: dict = {ETHEREUM: "0x8667DBEBf68B0BFa6Db54f550f41Be16c4067d60"}

    def __init__(self, blockchain, block) -> None:
        self.BLOCKCHAIN = blockchain
        self.ADDR = self.ADDRS[blockchain]
        super().__init__(block)

    def get_all_vault_managers_addrs(self) -> list[str]:
        """
        Returns all vault manager addresses from treasury.
        """
        nvault = 0
        vaults = []
        while True:
            try:
                vaults.append(self.vault_manager_list(nvault))
                nvault += 1
            except ContractLogicError as error:
                if error.message == "execution reverted":
                    logger.debug("End of vault manager list reachead")
                    break
                else:
                    raise ContractLogicError(error)
        return vaults


class Oracle(abstract.Oracle):
    def __init__(self, blockchain, address, block) -> None:
        self.BLOCKCHAIN = blockchain
        self.ADDR = address
        super().__init__(block)

    def get_decimals(self) -> int:
        if "EUR" in self.description:
            return 18
        else:
            raise ValueError("Not decimal specified")

    def rate(self) -> Decimal:
        return self.read / Decimal(10 ** self.get_decimals())


class VaultManager(abstract.VaultManager):
    def __init__(self, blockchain, address, block) -> None:
        self.BLOCKCHAIN = blockchain
        self.ADDR = address
        super().__init__(block)

    def vaults_owned_by(self, wallet: str) -> int:
        wallet = Web3.to_checksum_address(wallet)
        return self.balance_of(wallet)

    def get_oracle(self) -> Oracle:
        return Oracle(self.BLOCKCHAIN, self.oracle, self.block)

    def vault_ids_owned_by(self, wallet: str, vault_ids: list) -> bool:
        if self.vaults_owned_by(wallet) != len(vault_ids):
            return False
        for vault_id in vault_ids:
            if self.owner_of(vault_id) != wallet:
                return False
        return True

    @cache_contract_method(validator=vault_ids_owned_by)
    def get_vault_ids_from(self, wallet: str) -> list:
        wallet = Web3.to_checksum_address(wallet)
        vault_ids = []
        for vault_id in range(self.vault_id_count + 1):
            try:
                if wallet == self.owner_of(vault_id):
                    vault_ids.append(vault_id)
            except ContractCustomError as error:
                if error == "0x0c5473ba":
                    pass
                else:
                    ContractCustomError(error)
        return {"wallet": wallet, "vault_ids": vault_ids}

    def get_vault_data(self, vaultid: int, decimals: bool = True) -> dict:
        stablecoin_decimals = (
            get_decimals(self.stablecoin, self.BLOCKCHAIN, get_node(self.BLOCKCHAIN, self.block)) if decimals else 0
        )
        collateral_decimals = (
            get_decimals(self.collateral, self.BLOCKCHAIN, get_node(self.BLOCKCHAIN, self.block)) if decimals else 0
        )
        contract_decimals = str(self.base_params).count("0")
        interest_decimals = str(self.base_interest).count("0")

        collateral_factor = self.collateral_factor / Decimal(10**contract_decimals)

        debt = self.get_vault_debt(vaultid) / Decimal(10**stablecoin_decimals)

        collateral_deposit, normalized_debt = self.vault_data(vaultid)
        collateral_amount = collateral_deposit / Decimal(10**collateral_decimals)

        collateral_to_stablecoin = self.get_oracle().rate()
        collateral_in_stablecoin = collateral_deposit * collateral_to_stablecoin / Decimal(10**stablecoin_decimals)

        # health_factor = collateral_in_stablecoin * collateral_factor / debt

        available_to_borrow = collateral_in_stablecoin * collateral_factor - debt

        interest_rate_per_second = self.interest_rate / Decimal(10**interest_decimals)

        data = {
            "assets": [
                {"address": self.stablecoin, "balance": -debt},
                {"address": self.collateral, "balance": collateral_amount},
            ],
            "financial_metrics": {
                # "health_factor": health_factor,
                # "loan_to_value": debt / collateral_in_stablecoin,
                "collateral_ratio": collateral_in_stablecoin / debt,
                "liquidation_ratio": 1 / collateral_factor,
                "anual_interest_rate": interest_rate_per_second * 365 * 24 * 3600,
                "liquidation_price_in_stablecoin_fiat": debt / collateral_factor / collateral_amount,
                "available_to_borrow": {"address": self.stablecoin, "balance": available_to_borrow},
            },
        }
        return data


def underlying(blockchain: str, wallet: str, block: int | str = "latest", decimals: bool = True) -> dict:
    """
    TODO: Add documentation
    """
    wallet = Web3.to_checksum_address(wallet)
    treasury = Treasury(blockchain, block)

    positions = {}

    for vault_addr in treasury.get_all_vault_managers_addrs():
        vault_manager = VaultManager(blockchain, vault_addr, block)
        if vault_manager.vaults_owned_by(wallet) >= 1:
            vault_ids = vault_manager.get_vault_ids_from(wallet)["vault_ids"]
            for vault_id in vault_ids:
                vault_data = vault_manager.get_vault_data(vault_id, decimals=decimals)
                positions[str(vault_id)] = vault_data
    return {
        "protocol": "Angle",
        "blockchain": blockchain,
        "block": block,
        "positions_key": "vault_id",
        "positions": positions,
        "underlying_version": 0,
    }
