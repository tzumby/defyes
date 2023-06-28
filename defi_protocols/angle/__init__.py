from typing import Tuple

from defi_protocols.cache import const_call
from defi_protocols.functions import get_node


class BaseOracle:
    ABI: str = [
        {
            "inputs": [],
            "name": "DESCRIPTION",
            "outputs": [{"internalType": "string", "name": "", "type": "string"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "read",
            "outputs": [{"internalType": "uint256", "name": "quoteAmount", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    BLOCKCHAIN: str
    ADDR: str

    def __init__(self, block) -> None:
        node = get_node(self.BLOCKCHAIN, block)
        self.block = block
        self.contract = node.eth.contract(address=self.ADDR, abi=self.ABI)

    @property
    def description(self) -> str:
        return const_call(self.contract.functions.DESCRIPTION())

    @property
    def read(self) -> int:
        return self.contract.functions.read().call(block_identifier=self.block)


class BaseTreasury:
    ABI: str = [
        {
            "inputs": [],
            "name": "stablecoin",
            "outputs": [{"internalType": "contract IAgToken", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "vaultManagerList",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "address", "name": "_vaultManager", "type": "address"}],
            "name": "isVaultManager",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    BLOCKCHAIN: str
    ADDR: str

    def __init__(self, block) -> None:
        node = get_node(self.BLOCKCHAIN, block)
        self.block = block
        self.contract = node.eth.contract(address=self.ADDR, abi=self.ABI)

    @property
    def stablecoin(self) -> str:
        return const_call(self.contract.functions.stablecoin())

    def vault_manager_list(self, arg0: int) -> str:
        return self.contract.functions.vaultManagerList(arg0).call(block_identifier=self.block)

    def is_vault_manager(self, arg0: str) -> bool:
        return self.contract.functions.isVaultManager(arg0).call(block_identifier=self.block)


class BaseVaultManager:
    ABI: str = [
        {
            "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "vaultIDCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "vaultID", "type": "uint256"}],
            "name": "ownerOf",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "oracle",
            "outputs": [{"internalType": "contract IOracle", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "collateralFactor",
            "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "BASE_INTEREST",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "BASE_PARAMS",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "collateral",
            "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "vaultID", "type": "uint256"}],
            "name": "getVaultDebt",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "vaultData",
            "outputs": [
                {
                    "internalType": "uint256",
                    "name": "collateralAmount",
                    "type": "uint256",
                },
                {
                    "internalType": "uint256",
                    "name": "normalizedDebt",
                    "type": "uint256",
                },
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "stablecoin",
            "outputs": [{"internalType": "contract IAgToken", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "interestRate",
            "outputs": [{"internalType": "uint64", "name": "", "type": "uint64"}],
            "stateMutability": "view",
            "type": "function",
        },
    ]

    BLOCKCHAIN: str
    ADDR: str

    def __init__(self, block) -> None:
        node = get_node(self.BLOCKCHAIN, block)
        self.block = block
        self.contract = node.eth.contract(address=self.ADDR, abi=self.ABI)

    def balance_of(self, arg0: str) -> int:
        return self.contract.functions.balanceOf(arg0).call(block_identifier=self.block)

    @property
    def vault_id_count(self) -> int:
        return self.contract.functions.vaultIDCount().call(block_identifier=self.block)

    def owner_of(self, arg0: int) -> str:
        return self.contract.functions.ownerOf(arg0).call(block_identifier=self.block)

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

    def get_vault_debt(self, arg0: int) -> int:
        return self.contract.functions.getVaultDebt(arg0).call(block_identifier=self.block)

    def vault_data(self, arg0: int) -> Tuple[int, int]:
        # Output: collateralAmount, normalizedDebt
        return self.contract.functions.vaultData(arg0).call(block_identifier=self.block)

    @property
    def stablecoin(self) -> str:
        return const_call(self.contract.functions.stablecoin())

    @property
    def interest_rate(self) -> int:
        return self.contract.functions.interestRate().call(block_identifier=self.block)
