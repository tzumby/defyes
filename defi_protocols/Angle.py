import logging

from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar, Dict, List
from web3.contract import Contract
from web3.exceptions import ContractLogicError

from defi_protocols.cache import const_call
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_node, get_contract


logger = logging.getLogger(__name__)

# Borrow Module
# https://docs.angle.money/angle-borrowing-module/borrowing-module
# https://github.com/AngleProtocol/borrow-contracts/tree/main
@dataclass
class Treasury:
    ABI: ClassVar[str] = """[{"inputs":[],\
                              "name":"stablecoin",\
                              "outputs":[{"internalType":"contract IAgToken","name":"","type":"address"}],\
                              "stateMutability":"view","type":"function"},\
                             {"inputs":[{"internalType":"uint256", "name":"","type":"uint256"}],\
                              "name":"vaultManagerList",\
                              "outputs":[{"internalType":"address","name":"","type":"address"}],\
                              "stateMutability":"view","type":"function"\
                             }\
                            ]"""
    ADDRS: ClassVar[Dict] = {ETHEREUM: "0x8667DBEBf68B0BFa6Db54f550f41Be16c4067d60"}
    blockchain: str
    block: int | str
    addr: str = field(init=False)
    contract: Contract = field(init=False)
    stablecoin_addr: str = field(init=False)
    vault_managers: List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.addr = self.ADDRS[self.blockchain]
        self.contract = get_contract(self.addr, self.blockchain, abi=self.ABI, block=self.block)
        self.stablecoin_addr = const_call(self.contract.functions.stablecoin())
        self.vault_managers = self.get_vault_managers()

    def get_vault_managers(self):
        nvault = 0
        vaults = []
        while True:
            try:
                vaults.append(const_call(self.contract.functions.vaultManagerList(nvault)))
                nvault += 1
            except ContractLogicError as error:
                if error.message == 'execution reverted':
                    logger.debug('End of vault manager list reachead')
                    break
                else:
                    raise ContracLogicError(error)
        return vaults

