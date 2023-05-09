from defi_protocols.functions import get_contract, balance_of, get_node, get_decimals, last_block
from defi_protocols.constants import ETHEREUM, XDAI
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
from dataclasses import dataclass, field
from typing import Union
# thegraph queries
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SUBGRAPH API ENDPOINTS
# https://docs.connext.network/developers/guides/xcall-status
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mainnet - Subgraph API endpoint
SUBGRAPH_API_ENDPOINT_ETH = 'https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-mainnet'

# GC - Subgraph API endpoint
SUBGRAPH_API_ENDPOINT_GC = 'https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-gnosis'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONNEXT DIAMOND ADDRESSES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mainnet - Connext Diamond Address
CONNEXT_DIAMOND_ETH = '0x8898B472C54c31894e3B9bb83cEA802a5d0e63C6'

# GC - Connext Diamond Address
CONNEXT_DIAMOND_GC = '0x5bB83e95f63217CDa6aE3D181BA580Ef377D2109'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Connext Diamond ABI - getSwapLPToken, getSwapTokenIndex, getSwapToken, calculateRemoveSwapLiquidity
ABI_CONNEXT_DIAMOND = '[{"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"}],"name":"getSwapLPToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"getSwapTokenIndex","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"uint8","name":"index","type":"uint8"}],"name":"getSwapToken","outputs":[{"internalType":"contractIERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"calculateRemoveSwapLiquidity","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]'


def call_contract_method(method, block):
    try:
        return method.call(block_identifier = block)
    except Exception as e:
        if type(e) == ContractLogicError or type(e) == BadFunctionCallOutput or \
                (type(e) == ValueError and (e.args[0]['code'] == -32000 or e.args[0]['code'] == -32015)):
            return None
        else:
            raise e


def query_assets(subgraph_api_endpoint: str, web3: object) -> list:
    """Return a list of dict:assets with it's id, key, adoptedAsset and decimals

    Args:
        subgraph_api_endpoint (str): Subgraph API endpoint

    Returns:
        list: list of dict:assets with it's id, key, adoptedAsset and decimals
    """
    assets = []
    skip = 0
    first = 1000
    status = 'true'

    # Initialize subgraph
    connext_transport=RequestsHTTPTransport(
            url=subgraph_api_endpoint,
            verify=True,
            retries=3
        )
    client = Client(transport=connext_transport)
    
    response_length = 1001
    
    while not response_length < 1000:
        query_string = f'''
        query {{
        assets(first: {first}, skip: {skip}, where: {{status_:{{status: {status}}}}}) {{
            id
            key
            adoptedAsset
            decimal
            status {{status}}
        }}
        }}
        '''

        #formatted_query_string = query_string.format(first=assets_to_query, skip=skip)
        response = client.execute(gql(query_string))
        assets.extend(response['assets'])
        response_length = len(response['assets'])
        skip += response_length
        
    for a in assets:
        a['id'] = web3.to_checksum_address(a['id'])
        a['adoptedAsset'] = web3.to_checksum_address(a['adoptedAsset'])
        a['decimal'] = int(a['decimal']) if a.get('decimal', None) else 0

    return assets


@dataclass
class Connext():
    blockchain: str
    block: int|str
    diamond_adrr: str = field(init=False)
    diamond_contract: object = field(init=False)
    subgraph_api_endpoint: str = field(init=False)
    assets: list = field(init=False)

    def __post_init__(self) -> None:
        if self.blockchain == ETHEREUM:
            self.diamond_adrr = CONNEXT_DIAMOND_ETH
            self.subgraph_api_endpoint = SUBGRAPH_API_ENDPOINT_ETH
        elif self.blockchain == XDAI:
            self.diamond_adrr = CONNEXT_DIAMOND_GC
            self.subgraph_api_endpoint = SUBGRAPH_API_ENDPOINT_GC
        else:
            raise ValueError(f"{self.blockchain} not supported yet")
        
        self.web3 = get_node(self.blockchain, self.block)
        self.diamond_contract = get_contract(self.diamond_adrr, self.blockchain, web3=self.web3, abi=ABI_CONNEXT_DIAMOND, block=self.block)
        self.assets = query_assets(self.subgraph_api_endpoint, self.web3)

    def underlying(self, wallet: str, lptoken_address: str, decimals: bool = True) -> list:
        """Returns the underlying token balances for the given wallet, lp token address

        Returns:
            list: list of tuples containing [underlying_token_address, balance]
        """
        balances = []
        
        wallet = self.web3.to_checksum_address(wallet)
        lptoken_address = self.web3.to_checksum_address(lptoken_address)

        for asset in self.assets:
            if  lptoken_address == self.diamond_contract.functions.getSwapLPToken(asset['key']).call():
                lptoken_balance = balance_of(wallet, lptoken_address, self.block, self.blockchain, decimals=False)
                amounts = call_contract_method(self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset['key'], lptoken_balance), self.block)

                if not amounts:
                    return [[asset['id'], 0], [asset['adoptedAsset'], 0]]
                
                if decimals:
                    amounts = [amount/(10**asset['decimal']) for amount in amounts]

                return [[asset['id'], amounts[0]], [asset['adoptedAsset'], amounts[1]]]
        
        return balances

    def underlying_all(self, wallet: str, decimals: bool = True) -> list:
        """Returns the underlying token balances for all the lp tokens in the protocol for the given wallet and blockchain

        Returns:
            list: list: list of tuples containing [underlying_token_address, balance]
        """
        balances = []
        
        wallet = self.web3.to_checksum_address(wallet)

        for asset in self.assets:
            lptoken_address = self.diamond_contract.functions.getSwapLPToken(asset['key']).call()
            lptoken_balance = balance_of(wallet, lptoken_address, self.block, self.blockchain, decimals=False)
            amounts = call_contract_method(self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset['key'], lptoken_balance), self.block)
            
            if (not amounts) or amounts == [0,0]:
                continue

            if decimals:
                amounts = [amount/(10**asset['decimal']) for amount in amounts]

            balances.append([[asset['id'], amounts[0]], [asset['adoptedAsset'], amounts[1]]])
        
        return balances
    
    def unwrap(self, lptoken_amount: float, lptoken_address: str, decimals: bool = True) -> list:    
        """Returns the unwrapped amount of underlying token given an lp token amount and address

        Returns:
            list: underlying_token, unwrapped_amount
        """
        
        lptoken_address = self.web3.to_checksum_address(lptoken_address)

        for asset in self.assets:
            if  lptoken_address == self.diamond_contract.functions.getSwapLPToken(asset['key']).call():
                lptoken_decimals = get_decimals(lptoken_address, self.blockchain, web3=self.web3)
                amounts = call_contract_method(self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset['key'], int(lptoken_amount*(10**lptoken_decimals))), self.block)

                if not amounts:
                    return 0
                
                if decimals:
                    amounts = [amount/(10**asset['decimal']) for amount in amounts]

                return [asset['adoptedAsset'], amounts[0]+amounts[1]]
        
        return []


# Transitional wrapper of underlying method
def underlying(wallet: str, lptoken_address: str, block: int|str, blockchain: str, web3=None, decimals: bool = True) -> list:
    connext = Connext(blockchain, block)

    return connext.underlying(wallet, lptoken_address, decimals)

def underlying_all(wallet: str, block: int|str, blockchain: str, web3=None, decimals: bool = True) -> list:
    connext = Connext(blockchain, block)

    return connext.underlying_all(wallet, decimals)

def unwrap(lptoken_amount: float, lptoken_address: str, block: int|str, blockchain: str, web3=None, decimals: bool = True) -> list:
    connext = Connext(blockchain, block)

    return connext.unwrap(lptoken_amount, lptoken_address, decimals)
