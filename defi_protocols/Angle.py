import logging

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List
from web3.exceptions import ContractLogicError, ContractCustomError
from web3 import Web3

from defi_protocols.constants import ETHEREUM
from defi_protocols.contract import DefiContract
from defi_protocols.functions import get_decimals


logger = logging.getLogger(__name__)

# Borrow Module
# https://docs.angle.money/angle-borrowing-module/borrowing-module
# https://github.com/AngleProtocol/borrow-contracts/tree/main

@dataclass
class Asset:
    network: str
    id: str
    amount: Decimal

    def __repr__(self):
        return f'<Asset: {self.amount} of token {self.id} in {self.network} network>'

class Treasury(DefiContract):
    # https://developers.angle.money/borrowing-module-contracts/smart-contract-docs/treasury
    # https://github.com/AngleProtocol/borrow-contracts/tree/main/contracts/treasury
    ABI: str = """[{"inputs":[],\
                    "name":"stablecoin",\
                    "outputs":[{"internalType":"contract IAgToken","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[{"internalType":"uint256", "name":"","type":"uint256"}],\
                    "name":"vaultManagerList",\
                    "outputs":[{"internalType":"address","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"\
                   }\
                  ]"""
    ADDRS: Dict = {ETHEREUM: "0x8667DBEBf68B0BFa6Db54f550f41Be16c4067d60"}

    def __init__(self, blockchain) -> None:
        super().__init__(blockchain, self.ADDRS[blockchain])

    @property
    def stable_token(self):
        return self.stablecoin().const_call()

    def get_all_vault_managers_addrs(self, block) -> List[str]:
        """
        Returns all vault manager addresses from treasury.
        """
        nvault = 0
        vaults = []
        while True:
            try:
                vaults.append(self.vaultManagerList(nvault).const_call())
                nvault += 1
            except ContractLogicError as error:
                if error.message == 'execution reverted':
                    logger.debug('End of vault manager list reachead')
                    break
                else:
                    raise ContracLogicError(error)
        return vaults


class Oracle(DefiContract):
    ABI: str = """[{"inputs": [],\
                    "name": "DESCRIPTION",\
                    "outputs": [{"internalType": "string", "name": "", "type": "string"}],\
                    "stateMutability": "view","type": "function"},\
                   {"inputs": [],\
                    "name": "read",\
                    "outputs": [{"internalType": "uint256", "name": "quoteAmount", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"}\
                  ]"""

    def __init__(self, blockchain, address) -> None:
        super().__init__(blockchain, address)
        self.decimals = self.get_decimals()

    def get_decimals(self) -> int:
        description = self.DESCRIPTION().const_call()
        if 'EUR' in description:
            return 18
        else:
            raise ValueError('Not decimal specified')

    @property
    def rate(self) -> Decimal:
        return self.read().call() / Decimal(10 ** self.decimals)


class VaultManager(DefiContract):
    ABI: str = """[{"inputs": [{"internalType": "address", "name": "owner", "type": "address"}],\
                    "name": "balanceOf",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs":[],\
                    "name":"vaultIDCount",\
                    "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[{"internalType":"uint256","name":"vaultID","type":"uint256"}],\
                    "name":"ownerOf",\
                    "outputs":[{"internalType":"address","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs":[],\
                    "name":"oracle",\
                    "outputs":[{"internalType":"contract IOracle","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs": [],\
                    "name": "collateralFactor",\
                    "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "BASE_INTEREST",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "BASE_PARAMS",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [],\
                    "name": "collateral",\
                    "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [{"internalType": "uint256", "name": "vaultID", "type": "uint256"}],\
                    "name": "getVaultDebt",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                    "stateMutability": "view", "type": "function"},\
                   {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],\
                    "name": "vaultData",\
                    "outputs": [{"internalType": "uint256", "name": "collateralAmount", "type": "uint256"},\
                                {"internalType": "uint256", "name": "normalizedDebt", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs":[],\
                    "name":"stablecoin",\
                    "outputs":[{"internalType":"contract IAgToken","name":"","type":"address"}],\
                    "stateMutability":"view","type":"function"},\
                   {"inputs": [],\
                    "name": "interestRate",\
                    "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],\
                    "stateMutability": "view", "type": "function"}\
                  ]"""

    def __init__(self, blockchain, address) -> None:
        super().__init__(blockchain, address)

    def has_vaults_owned_by(self, wallet: str, block: int| str) -> bool:
        wallet = Web3.to_checksum_address(wallet)
        return self.balanceOf(wallet).call(block_identifier=block) >= 1

    @property
    def stable_token(self):
        return self.stablecoin().const_call()

    @property
    def collateral_token(self):
        return self.collateral().const_call()

    def get_oracle(self) -> Oracle:
        return Oracle(self.blockchain, self.oracle().const_call())

    def get_vault_data(self, vaultid: int, block: int) -> Dict:
        stablecoin_decimals = get_decimals(self.stable_token, self.blockchain, self.get_node(block))
        collateral_decimals = get_decimals(self.collateral_token, self.blockchain, self.get_node(block))
        contract_decimals = str(self.BASE_PARAMS().const_call()).count('0')
        interest_decimals = str(self.BASE_INTEREST().const_call()).count('0')

        collateral_factor = self.collateralFactor().call(block_identifier=block) / Decimal(10 ** contract_decimals)

        debt = self.getVaultDebt(vaultid).call(block_identifier=block) / Decimal(10 ** stablecoin_decimals)

        collateral_deposit, normalized_debt = self.vaultData(vaultid).call(block_identifier=block)
        collateral_amount = collateral_deposit / Decimal(10 **collateral_decimals)

        collateral_to_stablecoin = self.get_oracle().rate
        collateral_in_stablecoin = collateral_deposit * collateral_to_stablecoin / Decimal(10 ** stablecoin_decimals)

        health_factor = collateral_in_stablecoin * collateral_factor / debt

        available_to_borrow = collateral_in_stablecoin * collateral_factor - debt

        interest_rate_per_second = self.interestRate().call(block_identifier=block) / Decimal(10 ** interest_decimals)

        return {'debt': Asset(self.blockchain, self.stable_token, debt),
                'available_to_borrow': Asset(self.blockchain, self.stable_token, available_to_borrow),
                'collateral_deposit': Asset(self.blockchain, self.collateral_token, collateral_amount),
                'health_factor': health_factor, 'loan_to_value': debt / collateral_in_stablecoin,
                'anual_interest_rate': interest_rate_per_second * 365 * 24 * 3600,
                'liquidation_price_in_stablecoin_fiat': debt / collateral_factor / collateral_amount}


def underlying(blockchain: str, wallet: str, block: int | str) -> None:
    """
    Returns the list of vault_manager contracts in which the wallet owns at least a Vault.
    """
    wallet = Web3.to_checksum_address(wallet)
    treasury = Treasury(blockchain)

    equivalent_amount = 0
    equivalent_unit = 'EUR'  # TODO: make unit a parameter the user can choose
    positions = []

    for vault_addr in treasury.get_all_vault_managers_addrs(block):

        vault_manager = VaultManager(blockchain, vault_addr)
        if vault_manager.has_vaults_owned_by(wallet, block):

            vaults = vault_manager.vaultIDCount().call(block_identifier=block)
            for vault_id in range(vaults + 1):
                try:
                    if wallet == vault_manager.ownerOf(vault_id).call(block_identifier=block):
                        vault_data = vault_manager.get_vault_data(vault_id, block)
                        equivalent_amount += vault_data['available_to_borrow'].amount
                        positions.append(vault_data)
                except ContractCustomError as error:
                    if error == '0x0c5473ba':
                        pass
                    else:
                        ContractCustomError(error)

    return {'equivalent_amount': equivalent_amount, 'equivalent_uint': equivalent_unit, 'positions': positions}
