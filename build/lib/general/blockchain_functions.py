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
class GetNodeIndexError(Exception):
    pass



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_node
# 'block' = 'latest' -> retrieves a Full Node / 'block' = block or not passed onto the function -> retrieves an Archival Node
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_node(blockchain, block='latest', index=0):

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
    else:
        raise Exception

    if isinstance(block, str):
        if block == 'latest':
            if index > (len(node['latest']) - 1):
                if index > (len(node['latest']) + len(node['archival']) - 1):
                    raise GetNodeIndexError
                else:
                    web3 = Web3(Web3.HTTPProvider(node['archival'][index-len(node['archival'])]))
            else:
                web3 = Web3(Web3.HTTPProvider(node['latest'][index]))
        else:
            raise ValueError('Incorrect block.')

    else:
        if index > (len(node['archival']) - 1):
            raise GetNodeIndexError
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
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def last_block(blockchain, web3=None, block='latest', index=0):

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    return web3.eth.blockNumber


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_date
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_date(timestamp, utc=0):

    return datetime.utcfromtimestamp(timestamp + 3600 * utc).strftime('%Y-%m-%d %H:%M:%S')


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_block
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_block(timestamp, blockchain) -> int:

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
            data = requests.get(API_ROPSTEN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']

    return int(data)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_timestamp
# 'utc' = timezone of the Input is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_timestamp(datestring, utc=0):

    #   localTimestamp = math.floor(time.mktime(datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S').timetuple()) + 3600 * utc)
    utc_timestamp = math.floor(calendar.timegm(datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S').timetuple()) - 3600 * utc)

    return utc_timestamp


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_block
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_block(datestring, blockchain, utc=0) -> int:
    """

    :param str datestring:
    :param str blockchain:
    :param utc:
    :return:
    """
    return timestamp_to_block(date_to_timestamp(datestring, utc=utc), blockchain)


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
# 'utc' = timezone of the Output is UTC(+'utc')
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_to_date(block, blockchain, utc=0):

    return timestamp_to_date(block_to_timestamp(block, blockchain), utc=utc)


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
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def balance_of(address, contract_address, block, blockchain, web3=None, index=0, decimals=True):

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    address = web3.toChecksumAddress(address)

    contract_address = web3.toChecksumAddress(contract_address)

    if contract_address == ZERO_ADDRESS:
        if decimals is True:
            return web3.eth.get_balance(address, block) / (10 ** 18)
        else:
            web3.eth.get_balance(address, block)

    else:
        token_contract = web3.eth.contract(address=contract_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))

        if decimals is True:
            token_decimals = token_contract.functions.decimals().call()
        else:
            token_decimals = 0

        try:
            balance = token_contract.functions.balanceOf(address).call(block_identifier=block)
        except:
            balance = 0

        return balance / (10 ** token_decimals)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# total_supply
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def total_supply(token_address, block, blockchain, web3=None, index=0, decimals=True):

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    if not web3.isChecksumAddress(token_address):
        token_address = web3.toChecksumAddress(token_address)

    token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
    total_supply = token_contract.functions.totalSupply().call(block_identifier=block)

    if decimals is True:
        token_decimals = token_contract.functions.decimals().call(block_identifier=block)
    else:
        token_decimals = 0

    return total_supply / (10 ** token_decimals)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_decimals
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_decimals(token_address, blockchain, web3=None, block='latest', index=0):

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    token_address = web3.toChecksumAddress(token_address)

    if token_address == ZERO_ADDRESS:
        decimals = 18
    else:
        token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
        decimals = token_contract.functions.decimals().call()

    return decimals


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_symbol
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_symbol(token_address, blockchain, web3=None, block='latest', index=0) -> str:
    """

    :param str token_address:
    :param str blockchain:
    :param web3:
    :param block:
    :param int index:
    :return:
    """

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    token_address = web3.toChecksumAddress(token_address)

    if token_address == ZERO_ADDRESS or token_address == E_ADDRESS:
        if blockchain == ETHEREUM:
            symbol = 'ETH'
        elif blockchain == POLYGON:
            symbol = 'MATIC'
        elif blockchain == XDAI:
            symbol = 'XDAI'
    else:
        token_contract = web3.eth.contract(address=token_address, abi=ABI_TOKEN_SIMPLIFIED)

        try:
            symbol = token_contract.functions.symbol().call()
        except:
            try:
                symbol = token_contract.functions.SYMBOL().call()
            except:
                try:
                    token_contract = web3.eth.contract(address=token_address, abi=get_contract_abi(token_address, blockchain))
                    symbol = token_contract.functions.symbol().call()
                except:
                    print('Token %s has no symbol()' % token_address)
                    symbol = ''

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
            data = requests.get(API_GNOSISSCAN_GETABI % (contract_address, API_KEY_GNOSISSCAN)).json()['result']
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
            data = requests.get(API_ROPSTEN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()['result']
            if data == 'Contract source code not verified':
                print('Error: Contract source code not verified')
                return None

    return data


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract
# 'web3' = web3 (Node) -> Improves performance
# 'abi' = specifies the exact ABI (used when contracts are not verified)
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract(contract_address, blockchain, web3=None, abi=None, block='latest', index=0):
    
    if web3 == None: 
        web3 = get_node(blockchain, block=block, index=index)

    contract_address = web3.toChecksumAddress(contract_address)

    if abi == None: 
        abi = get_contract_abi(contract_address, blockchain)

    return web3.eth.contract(address=contract_address, abi=abi)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract_proxy_abi
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract_proxy_abi(contract_address, abi_contract_address, blockchain, web3=None, block='latest', index=0):

    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    address = web3.toChecksumAddress(contract_address)

    return web3.eth.contract(address=address, abi=get_contract_abi(abi_contract_address, blockchain))


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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_block_samples(start_date, samples, blockchain, end_date='latest', utc=0, dates=False):
    start_timestamp = date_to_timestamp(start_date, utc=utc)
    if end_date == 'latest':
        end_timestamp = math.floor(datetime.now().timestamp())
    else:
        end_timestamp = date_to_timestamp(end_date, utc=utc)

    period = int((end_timestamp - start_timestamp) / (samples - 1))

    timestamps = [start_timestamp + i * period for i in range(samples)]

    dates_strings = [datetime.utcfromtimestamp(timestamp + 3600 * utc).strftime('%Y-%m-%d %H:%M:%S') for timestamp in
             timestamps]

    blocks = [timestamp_to_block(timestamps[i], blockchain) for i in range(samples)]

    if dates is True:
        return [blocks, dates_strings]
    else:
        return blocks

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LPTOKENSDATABASE = blockchain_database.LPTOKENSDATABASE

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# liquidity tokens and pools
#These functions will be deleted in the near future, along with LPTOKENS_DATABASE and blockchain_database.py

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

    return lptoken_underlying(web3.toChecksumAddress(lptoken_address), balance_of(address, web3.toChecksumAddress(lptoken_address), block, blockchain), block)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def is_archival(endpoint) -> bool:
    """
    Checks whether a node is an archival node or a full node.

    :param str endpoint: The node's RPC endpoint to analyse
    :return: True if the node is archival, False if it isn't
    """

    web3 = Web3(Web3.HTTPProvider(endpoint))

    try:
        web3.eth.get_balance('0x849D52316331967b6fF1198e5E32A0eB168D039d', block_identifier=1)
    except ValueError:
        return False
    return True

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------