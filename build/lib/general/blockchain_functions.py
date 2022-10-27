from general.general_constants import *
from db import blockchain_database

from web3 import Web3
import requests

import json
import traceback

from datetime import datetime
import calendar

import math


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CUSTOM EXCEPTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class GetNodeLatestIndexError(Exception):
    pass

class GetNodeArchivalIndexError(Exception):
    pass
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_node
# **kwargs:
# 'block' = 'latest' -> retrieves a Full Node / 'block' = block or not passed onto the function -> retrieves an Archival Node
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_node(blockchain, **kwargs):
    
    if blockchain == ETHEREUM:
        node = NODE_ETH

    elif blockchain == POLYGON:
        node = NODE_POL

    elif blockchain == XDAI:
        node = NODE_XDAI

    elif blockchain == BINANCE:
        node = NODE_BINANCE

    elif blockchain == AVALANCHE:
        node = NODE_AVALANCHE

    elif blockchain == FANTOM:
        node = NODE_FANTOM

    elif blockchain == ROPSTEN:
        node = NODE_ROPSTEN

    elif blockchain == KOVAN:
        node = NODE_KOVAN

    elif blockchain == GOERLI:
        node = NODE_GOERLI

    try:
        block = kwargs['block']
    except:
        block = 'latest'

    try:
        index = kwargs['index']
    except:
        index = 0

    if isinstance(block, str):
        if block == 'latest':
            if index > (len(node['latest']) - 1):
                raise GetNodeLatestIndexError
            else:
                web3 = Web3(Web3.HTTPProvider(node['latest'][index]))

    else:
        if index > (len(node['archival']) - 1):
            raise GetNodeArchivalIndexError
        else:
            web3 = Web3(Web3.HTTPProvider(node['archival'][index]))

    return web3 

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_price_zapper - Test
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price_zapper():
    
    data = requests.get('https://api.zapper.fi/v2/prices/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48?network=ethereum&timeFrame=hour&currency=USD&api_key=04a45cb5-16d6-4d28-9ccc-e68ed47270f3').json()['prices']
    print(data)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# last_block
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def last_block(blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            block = kwargs['block']
        except:
            block = 'latest'

        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)

    return web3.eth.blockNumber

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_date
# **kwargs:
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_date(timestamp, **kwargs):
    
    try:
        utc = kwargs['utc']
    except:
        utc = 0

    return datetime.utcfromtimestamp(timestamp + 3600 * utc).strftime('%Y-%m-%d %H:%M:%S')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_block
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_block(timestamp, blockchain):
    
    data = None

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN)).json()['result']

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_POLSCAN)).json()['result']

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_GNOSISSCAN)).json()['result']
            # For BLOCKSCOUT
            # if data is None:
            #     time.sleep(0.1)
            # else:
            #     data = data['blockNumber']

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETBLOCKNOBYTIME % (timestamp, API_KEY_BINANCE)).json()['result']

        elif blockchain == AVALANCHE:
            data = requests.get(API_AVALANCHE_GETBLOCKNOBYTIME % (timestamp, API_KEY_AVALANCHE)).json()['result']

        elif blockchain == FANTOM:
            data = requests.get(API_FANTOM_GETBLOCKNOBYTIME % (timestamp, API_KEY_FANTOM)).json()['result']

        elif blockchain == ROPSTEN:
            data = requests.get(API_ROPSTEN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']

    return int(data)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_timestamp
# **kwargs:
# 'utc' = timezone of the Input is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_timestamp(datestring, **kwargs):
    
    try:
        utc = kwargs['utc']
    except:
        utc = 0

    #   localTimestamp = math.floor(time.mktime(datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S').timetuple()) + 3600 * utc)
    utc_timestamp = math.floor(
        calendar.timegm(datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S').timetuple()) - 3600 * utc)

    return utc_timestamp

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_block
# **kwargs:
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_block(datestring, blockchain, **kwargs):
    
    try:
        utc = kwargs['utc']
    except:
        utc = 0

    return timestamp_to_block(date_to_timestamp(datestring, utc = utc), blockchain)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# block_to_timestamp
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_to_timestamp(block, blockchain):
    
    data = None

    if isinstance(block, str):
        if block == 'latest':
            return math.floor(datetime.now().timestamp())

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN)).json()['result']['timeStamp']

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETBLOCKREWARD % (block, API_KEY_POLSCAN)).json()['result']['timeStamp']

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETBLOCKREWARD % (block, API_KEY_GNOSISSCAN)).json()['result']['timeStamp']

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETBLOCKREWARD % (block, API_KEY_BINANCE)).json()['result']['timeStamp']
        
        elif blockchain == AVALANCHE:
            data = requests.get(API_AVALANCHE_GETBLOCKREWARD % (block, API_KEY_AVALANCHE)).json()['result']['timeStamp']

        elif blockchain == ROPSTEN:
            data = requests.get(API_ROPSTEN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']['timeStamp']

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']['timeStamp']

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']['timeStamp']

    return int(data)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# block_to_date
# **kwargs:
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_to_date(block, blockchain, **kwargs):
    
    try:
        utc = kwargs['utc']
    except:
        utc = 0

    return timestamp_to_date(block_to_timestamp(block, blockchain), utc = utc)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_blocks_per_year
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_blocks_per_year(blockchain):
    
    current_block = last_block(blockchain)
    ts = math.floor(datetime.now().timestamp()) - (3600 * 24 * 365)
    block = timestamp_to_block(ts, blockchain)

    block_delta = current_block - block
    
    return block_delta


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERC20 TOKENS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# token_info
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def token_info(token_address, blockchain):  # NO ESTÁ POLYGON

    if blockchain.lower() == ETHEREUM:
        data = requests.get(API_ETHPLORER_GETTOKENINFO % (token_address, API_KEY_ETHPLORER)).json()

    elif blockchain.lower() == XDAI:
        data = requests.get(API_BLOCKSCOUT_GETTOKENCONTRACT % token_address).json()['result']

    return data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# balance_of
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def balance_of(address, contract_address, block, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    if not web3.isChecksumAddress(address):
        address = web3.toChecksumAddress(address)
    
    if not web3.isChecksumAddress(contract_address):
        contract_address = web3.toChecksumAddress(contract_address)

    if contract_address == ZERO_ADDRESS:
        if decimals == True:
            return web3.eth.get_balance(address, block) / (10 ** 18)
        else:
            web3.eth.get_balance(address, block)

    else:
        token_contract = web3.eth.contract(address = contract_address, abi = json.loads(ABI_TOKEN_SIMPLIFIED))
        
        if decimals == True:
            token_decimals = token_contract.functions.decimals().call()
        else:
            token_decimals = 0

        try:
            balance = token_contract.functions.balanceOf(address).call(block_identifier = block)
        except:
            balance = 0

        return balance / (10 ** token_decimals)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# total_supply
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def total_supply(token_address, block, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    if not web3.isChecksumAddress(token_address):
        token_address = web3.toChecksumAddress(token_address)

    token_contract = web3.eth.contract(address = token_address, abi = json.loads(ABI_TOKEN_SIMPLIFIED))
    total_supply = token_contract.functions.totalSupply().call(block_identifier = block)
    
    if decimals == True:
        token_decimals = token_contract.functions.decimals().call(block_identifier = block)
    else:
        token_decimals = 0

    return total_supply / (10 ** token_decimals)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_decimals
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_decimals(token_address, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            block = kwargs['block']
        except:
            block = 'latest'

        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)
    
    if not web3.isChecksumAddress(token_address):
        token_address = web3.toChecksumAddress(token_address)

    if token_address == ZERO_ADDRESS:
        decimals = 18
    else:
        token_contract = web3.eth.contract(address = token_address, abi = json.loads(ABI_TOKEN_SIMPLIFIED))
        decimals = token_contract.functions.decimals().call()

    return decimals

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_symbol
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_symbol(token_address, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            block = kwargs['block']
        except:
            block = 'latest'

        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)
    
    if not web3.isChecksumAddress(token_address):
        token_address = web3.toChecksumAddress(token_address)

    if token_address == ZERO_ADDRESS or token_address == E_ADDRESS:
        if blockchain == ETHEREUM:
            symbol = 'ETH'
        elif blockchain == POLYGON:
            symbol = 'MATIC'
        elif blockchain == XDAI:
            symbol = 'XDAI'
    else:
        token_contract = web3.eth.contract(address = token_address, abi = ABI_TOKEN_SIMPLIFIED)
        
        try:
            symbol = token_contract.functions.symbol().call()
        except:
            token_contract = web3.eth.contract(address = token_address, abi = get_contract_abi(token_address, blockchain))
            symbol = token_contract.functions.symbol().call()

        if not isinstance(symbol, str):
            symbol = symbol.hex()
            symbol = bytes.fromhex(symbol).decode('utf-8').rstrip('\x00')

    return symbol


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRACTS AND ABIS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract_abi
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract_abi(contract_address, blockchain):
   
    data = None

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETABI % (contract_address, API_KEY_ETHERSCAN)).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETABI % (contract_address, API_KEY_POLSCAN)).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETABI % (contract_address,API_KEY_GNOSISSCAN)).json()['result']
            if data == 'Contract source code not verified':
                data = requests.get(API_BLOCKSCOUT_GETABI % contract_address).json()['result']
                if data == 'Contract source code not verified':
                    print('Error: Contract source code not verified')
                    return None

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETABI % (contract_address, API_KEY_BINANCE)).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == ROPSTEN:
            data = requests.get(API_ROPSTEN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETABI % (contract_address, API_KEY_ETHERSCAN), headers = TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

    return data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract(contract_address, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            block = kwargs['block']
        except:
            block = 'latest'

        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)

    try:
        abi = kwargs['abi']
    except:
        abi = get_contract_abi(contract_address, blockchain)

    if not web3.isChecksumAddress(contract_address):
        contract_address = web3.toChecksumAddress(contract_address)

    return web3.eth.contract(address = contract_address, abi = abi)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract_proxy_abi
# **kwargs:
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract_proxy_abi(contract_address, abi_contract_address, blockchain, **kwargs):
    
    try:
        web3 = kwargs['web3']
    except:
        try:
            block = kwargs['block']
        except:
            block = 'latest'

        try:
            index = kwargs['index']
        except:
            index = 0

        web3 = get_node(blockchain, block = block, index = index)

    address = web3.toChecksumAddress(contract_address)

    return web3.eth.contract(address = address, abi = get_contract_abi(abi_contract_address, blockchain))


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCOUNTS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_token_tx
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_token_tx(token_address, contract_address, block_start, block_end, blockchain):
   
    data = None

    if blockchain == ETHEREUM:
        data = requests.get(API_ETHERSCAN_TOKENTX % (token_address, contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    elif blockchain == POLYGON:
        data = requests.get(API_POLYGONSCAN_TOKENTX % (token_address, contract_address, block_start, block_end, API_KEY_POLSCAN)).json()['result']

    elif blockchain == XDAI:
        data = requests.get(API_GNOSISSCAN_TOKENTX % (token_address, contract_address, block_start, block_end, API_KEY_GNOSISSCAN)).json()['result']

    return data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_tx_list
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_tx_list(contract_address, block_start, block_end, blockchain):
   
    data = None

    if blockchain == ETHEREUM:
        data = requests.get(API_ETHERSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    elif blockchain == POLYGON:
        data = requests.get(API_POLYGONSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_POLSCAN)).json()['result']

    elif blockchain == XDAI:
        data = requests.get(API_GNOSISSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_GNOSISSCAN)).json()['result']

    return data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LOGS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_logs
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_logs(block_start, block_end, address, topic0, blockchain, **kwargs):

    data = None
    optional_parameters = ''

    for key, value in kwargs.items():

        if key == 'topic1':
            if value:
                optional_parameters += '&topic1=%s' % (value)
                continue
        
        if key == 'topic2':
            if value:
                optional_parameters += '&topic2=%s' % (value)
                continue

        if key == 'topic3':
            if value:
                optional_parameters += '&topic3=%s' % (value)
                continue
        
        if key == 'topic0_1_opr':
            if value:
                optional_parameters += '&topic0_1_opr=%s' % (value)
                continue
        
        if key == 'topic0_2_opr':
            if value:
                optional_parameters += '&topic0_2_opr=%s' % (value)
                continue
        
        if key == 'topic0_3_opr':
            if value:
                optional_parameters += '&topic0_3_opr=%s' % (value)
                continue
        
        if key == 'topic1_2_opr':
            if value:
                optional_parameters += '&topic1_2_opr=%s' % (value) 
                continue
        
        if key == 'topic1_3_opr':
            if value:
                optional_parameters += '&topic1_3_opr=%s' % (value)
                continue
        
        if key == 'topic2_3_opr':
            if value:
                optional_parameters += '&topic2_3_opr=%s' % (value)
                continue

    
    if blockchain == ETHEREUM:
        data = requests.get(API_ETHERSCAN_GETLOGS % (block_start, block_end, address, topic0, API_KEY_ETHERSCAN) + optional_parameters).json()['result']

    elif blockchain == POLYGON:
        data = requests.get(API_POLYGONSCAN_GETLOGS % (block_start, block_end, address, topic0, API_KEY_POLSCAN) + optional_parameters).json()['result']

    elif blockchain == XDAI:
        data = requests.get(API_GNOSISSCAN_GETLOGS % (block_start, block_end, address, topic0, API_KEY_GNOSISSCAN) + optional_parameters).json()['result']
    
    elif blockchain == AVALANCHE:
        data = requests.get(API_AVALANCHE_GETLOGS % (block_start, block_end, address, topic0, API_KEY_AVALANCHE) + optional_parameters).json()['result']

    elif blockchain == BINANCE:
        data = requests.get(API_BINANCE_GETLOGS % (block_start, block_end, address, topic0, API_KEY_BINANCE) + optional_parameters).json()['result']
    
    elif blockchain == FANTOM:
        data = requests.get(API_FANTOM_GETLOGS % (block_start, block_end, address, topic0, API_KEY_FANTOM) + optional_parameters).json()['result']

    return data



LPTOKENSDATABASE = blockchain_database.LPTOKENSDATABASE

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# liquidity tokens and pools

def lptoken_underlying(lptoken_address, amount, block, blockchain):
    
    web3 = get_node(blockchain, block=block)
    index = [LPTOKENSDATABASE[i][1].lower() for i in range(len(LPTOKENSDATABASE))].index(lptoken_address.lower())
    poolAddress = web3.toChecksumAddress(LPTOKENSDATABASE[index][2])
    tokens = LPTOKENSDATABASE[index][3]
    fraction = amount / total_supply(web3.toChecksumAddress(lptoken_address), block, blockchain)

    return [[tokens[i], fraction * balance_of(poolAddress, tokens[i], block, blockchain)] for i in range(len(tokens))]

def pool_balance(lptoken_address, block, blockchain):
    
    web3 = get_node(blockchain, block=block)
    lptoken_address = web3.toChecksumAddress(lptoken_address)

    return lptoken_underlying(lptoken_address, total_supply(lptoken_address, block, blockchain), block, blockchain)

def balance_of_lptoken_underlying(address, lptoken_address, block, blockchain):
    
    web3 = get_node(blockchain, block=block)

    return lptoken_underlying(web3.toChecksumAddress(lptoken_address),
                             balance_of(address, web3.toChecksumAddress(lptoken_address), block, blockchain), block)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def is_archival(endpoint):
    web3 = Web3(Web3.HTTPProvider(endpoint))

    try:
        web3.eth.get_balance(ZERO_ADDRESS, block_identifier = 1)
    except ValueError:
        return False
    return True

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# web3=getNode(XDAI)
# Chef=getContract(web3.toChecksumAddress('0xdDCbf776dF3dE60163066A5ddDF2277cB445E0F3'),XDAI)
# Rewarder=getContract(web3.toChecksumAddress('0x3f505B5CfF05d04F468Db65e27E72EC45A12645f'),XDAI)
#
# rewardPerSecond=Rewarder.functions.rewardPerSecond().call()
# print('rewardPerSecond:',rewardPerSecond)
# allocPoint=Rewarder.functions.poolInfo(0).call()[2]
# print('allocPoint:',allocPoint)
# totalAllocPoint=Chef.functions.totalAllocPoint().call()
# print('totalAllocPoint:',totalAllocPoint)
# lpSupply=totalSupply(web3.toChecksumAddress('0xA227c72a4055A9DC949cAE24f54535fe890d3663'),'latest',XDAI)
# print('lpSupply:',lpSupply)
# print(rewardPerSecond*allocPoint/totalAllocPoint/lpSupply*10**(-18)*365*24*3600*1.20/2834265)
#print(isArchival('https://bsc.getblock.io/mainnet/?api_key=ec8f1352-32ad-4b35-a037-d899e5601b62'))

#print(Web3.keccak(text = 'Swap(address,uint256,uint256,uint256,uint256,address)').hex())

# gno_in = '0x52bbbe2900000000000000000000000000000000000000000000000000000000000000e00000000000000000000000004ef377462b03b650d52140c482394a6703d0d33800000000000000000000000000000000000000000000000000000000000000000000000000000000000000004ef377462b03b650d52140c482394a6703d0d33800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004fe2af19ead31900fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4c0dd9b82da36c07605df83c8a416f11724d88b00020000000000000000002600000000000000000000000000000000000000000000000000000000000000000000000000000000000000006810e776880c02933d47db1b9fc05908e5386b9600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000034a171d0245ed800000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000'
# gno_out = '0x52bbbe2900000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000d9a5c5bde6031f84422fbe53409804c403e1b1af0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d9a5c5bde6031f84422fbe53409804c403e1b1af0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000299fc58078021d69fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4c0dd9b82da36c07605df83c8a416f11724d88b000200000000000000000026000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000006810e776880c02933d47db1b9fc05908e5386b96000000000000000000000000000000000000000000000001a055690d9db8000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000000'

# print(gno_in.find(GNO_ETH[2:(len(GNO_ETH))].lower()))
# print(gno_out.find(GNO_ETH[2:(len(GNO_ETH))].lower()))


# gno_in = '0x56d3d2eb000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000021955b40017c2a000000000000000000000000000000000000000000000000000000000062d67117f4c0dd9b82da36c07605df83c8a416f11724d88b00020000000000000000002600000000000000000000000000000000000000000000000000000000000000000000000000000000000000006810e776880c02933d47db1b9fc05908e5386b96000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc200000000000000000000000000000000000000000000000153ac38521276000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
# gno_out = '0x56d3d2eb000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000021955b40017c2a000000000000000000000000000000000000000000000000000000000062d67117f4c0dd9b82da36c07605df83c8a416f11724d88b0002000000000000000000260000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc20000000000000000000000006810e776880c02933d47db1b9fc05908e5386b9600000000000000000000000000000000000000000000000153ac38521276000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

# print(gno_in.find(GNO_ETH[2:(len(GNO_ETH))].lower()))
# print(gno_out.find(GNO_ETH[2:(len(GNO_ETH))].lower()))

# hex = '00000000000000000000000000000000000000000000000133cad99c01e92d12'
# dec = int(hex, 16)

# print(dec)

# web3 = getNode(ETHEREUM)

# transaction = web3.eth.get_transaction('0xb71bbff0828ea61638ca4f20b90e089fee0b8bde5701d423d768e8f128c61e29')

# func = getattr(transaction, 'from')

# print(func)


# hex = 'dccb7a'
# dec = int(hex, 16)

# print(dec)

# hex = 'e77ff1'
# dec = int(hex, 16)

# print(dec)

# hex = 'e77ff6'
# dec = int(hex, 16)

# print(dec)

# hex = 'e77ff8'
# dec = int(hex, 16)

# print(dec)

#getLogs(15170000, 15171580, '0xba12222222228d8ba445958a75a0704d566bf2c8', '0x2170c741c41531aec20e7c107c24eecfdd15e69c9bb0a8dd37b1840b9e0b207b', ETHEREUM, topic1 = '0xf4c0dd9b82da36c07605df83c8a416f11724d88b000200000000000000000026', topic2 = '0x0000000000000000000000006810e776880c02933d47db1b9fc05908e5386b96', topic3 = '0x000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', topic0_1_opr = 'and', topic0_2_opr = 'and', topic0_3_opr = 'and')

# amounts = '0x000000000000000000000000000000000000000000000000296ce26901ad98c5000000000000000000000000000000000000000000000001a055690d9db80000'
# amount_in = int(amounts[2:66], 16)
# amount_out = int(amounts[67:130], 16)

# print(amount_in)
# print(amount_out)

#print(isArchival('https://bsc-mainnet.nodereal.io/v1/214197d3408f4bdda6568d5d414a59ae'))


# # UniswapV2
# print(Web3.keccak(text = 'Swap(address,uint256,uint256,uint256,uint256,address)').hex())

# # Balancer
# print(Web3.keccak(text = 'Swap(bytes32,address,address,uint256,uint256)').hex())

# # Curve
# print(Web3.keccak(text = 'TokenExchange(address,int128,uint256,int128,uint256)').hex())
# print(Web3.keccak(text = 'TokenExchange(address,uint256,uint256,uint256,uint256)').hex())

# print(Web3.keccak(text = 'TokenExchangeUnderlying(address,int128,uint256,int128,uint256)').hex())
# print(Web3.keccak(text = 'TokenExchangeUnderlying(address,uint256,uint256,uint256,uint256)').hex())
