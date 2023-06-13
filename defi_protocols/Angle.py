import logging
import json

from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar, Dict, List
from web3.contract import Contract
from web3.exceptions import ContractLogicError
from web3 import Web3

from defi_protocols.cache import const_call
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_node, get_contract


logger = logging.getLogger(__name__)


class DefiContractError(Exception):
    pass


class DefiContract:
    ABI = 'MUST_BE_DEFINED'
    CHAINED_FUNCS = ['call', 'const_call']

    def __init__(self, blockchain, address):
        self.blockchain = blockchain
        self.address = address
        self.contract_functions = [func['name'] for func in json.loads(self.ABI)]
        self.node = None
        self.contract = None

        self._attr = None
        self._function_call_data = {}

    def _update_node_and_contract(self, block):
        if self.node is None or block != self.node._called_with_block:
            self.node = get_node(self.blockchain, block)
            self.contract = self.node.eth.contract(address=self.address, abi=self.ABI)

    def __getattr__(self, attr):
        if attr in self.contract_functions + self.CHAINED_FUNCS:
            self._attr = attr
            return self
        else:
            raise AttributeError(f"'{self.__class__.__name__}' Object has no attribute '{attr}'")

    def __call__(self, *args, **kwargs):
        result = self

        if self._attr in self.contract_functions:
            self._function_call_data['method'] = {'name': self._attr, 'args': args, 'kwargs': kwargs}
        elif self._attr in self.CHAINED_FUNCS:
            if not self._function_call_data:
                raise DefiContractError(f'Executing chained function {self._attr} without proper definition of the first function.')

            block = kwargs.get('block_identifier', 'latest')
            self._update_node_and_contract(block)

            contract_fun = getattr(self.contract.functions, self._function_call_data['method']['name'])
            args_fun = self._function_call_data['method']['args']
            kwargs_fun = self._function_call_data['method']['kwargs']

            if self._attr == 'call':
                result = contract_fun(*args_fun, **kwargs_fun).call(**kwargs)
            elif self._attr == 'const_call':
                result = const_call(contract_fun(*args_fun, **kwargs_fun))

            self._function_call_data = {}

        return result


# Borrow Module
# https://docs.angle.money/angle-borrowing-module/borrowing-module
# https://github.com/AngleProtocol/borrow-contracts/tree/main
class Treasury(DefiContract):
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
    def stable_coin(self):
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


class VaultManager(DefiContract):
    ABI: str = """[{"inputs": [{"internalType": "address", "name": "owner", "type": "address"}],\
                    "name": "balanceOf",\
                    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],\
                    "stateMutability": "view", "type": "function"},\
                   {"inputs":[],\
                    "name":"vaultIDCount",\
                    "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],\
                    "stateMutability":"view","type":"function"}]"""

    def __init__(self, blockchain, address) -> None:
        super().__init__(blockchain, address)

    def has_vaults_owned_by(self, wallet: str, block: int| str) -> bool:
        wallet = Web3.to_checksum_address(wallet)
        return self.balanceOf(wallet).call(block_identifier=block) >= 1


def get_managers_and_vaultcounts(blockchain: str, wallet: str, block: int | str) -> None:
    """
    Returns the list of vault_manager contracts in which the wallet owns at least a Vault.
    """
    data = []
    treasury = Treasury(blockchain)

    for vault_addr in treasury.get_all_vault_managers_addrs(block):
        vault_manager = VaultManager(blockchain, vault_addr)
        if vault_manager.has_vaults_owned_by(wallet, block):
            data.append([vault_manager.address, vault_manager.vaultIDCount().call(block_identifier=block)])

    return data
