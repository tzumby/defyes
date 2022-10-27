from general.blockchain_functions import *
from defi_protocols import Elk
from defi_protocols import Honeyswap
from defi_protocols import Swapr
from defi_protocols import SushiSwap
import json
from pathlib import Path
import os
import eth_abi


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_token_mapping
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_token_mapping(token_address_eth, token_address_pol, token_address_xdai, **kwargs):

    try:
        price_feed_source = kwargs['price_feed_source']
    except:
        price_feed_source = None

    try:
        price_feed_blockchain = kwargs['price_feed_blockchain']
    except:
        price_feed_blockchain = None
    
    try:
        price_feed_connector = kwargs['price_feed_connector']
    except:
        price_feed_connector = None

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/token_mapping.json', 'r') as db_file:
        # Reading from json file
        db_data = json.load(db_file)
        db_file.close()
    
    web3 = get_node(ETHEREUM)

    if token_address_xdai != None and len(str(token_address_xdai)) > 0:
        if not web3.isChecksumAddress(token_address_xdai):
            token_address_xdai = web3.toChecksumAddress(token_address_xdai)
    
    if token_address_eth != None and len(str(token_address_eth)) > 0:
        if not web3.isChecksumAddress(token_address_eth):
            token_address_eth = web3.toChecksumAddress(token_address_eth)
    
    if token_address_pol != None and len(str(token_address_pol)) > 0:
        if not web3.isChecksumAddress(token_address_pol):
            token_address_pol = web3.toChecksumAddress(token_address_pol)

    # XDAI Node
    if token_address_xdai != None and len(str(token_address_xdai)) > 0:
        token_symbol = get_symbol(token_address_xdai, XDAI)

        try:
            token_data = db_data[XDAI][token_address_xdai]
            
            if token_address_eth != None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth
            
            if token_address_pol != None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol
            
            token_data['symbol'] = token_symbol

            try:
                price_feed_data = db_data[XDAI][token_address_xdai]['price_feed']

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector
            
            except:
                price_feed_data = {}

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector

                if price_feed_data != {}:
                    db_data[XDAI][token_address_xdai]['price_feed'] = price_feed_data
        
        except:
            token_data = {}
            price_feed_data = {}

            if token_address_eth != None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth
            
            if token_address_pol != None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol
            
            token_data['symbol'] = token_symbol

            if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

            if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
            if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                price_feed_data['connector'] = price_feed_connector

            if price_feed_data != {}:
                token_data['price_feed'] = price_feed_data

            db_data[XDAI][token_address_xdai] = token_data

    # ETHEREUM Node
    if token_address_eth != None and len(str(token_address_eth)) > 0:
        token_symbol = get_symbol(token_address_eth, ETHEREUM)

        try:
            token_data = db_data[ETHEREUM][token_address_eth]
            
            if token_address_xdai != None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai
            
            if token_address_pol != None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol
            
            token_data['symbol'] = token_symbol

            try:
                price_feed_data = db_data[ETHEREUM][token_address_eth]['price_feed']

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector
            
            except:
                price_feed_data = {}

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector

                if price_feed_data != {}:
                    db_data[ETHEREUM][token_address_eth]['price_feed'] = price_feed_data
        
        except:
            token_data = {}
            price_feed_data = {}

            if token_address_xdai != None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai
            
            if token_address_pol != None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol
            
            token_data['symbol'] = token_symbol

            if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

            if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
            if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                price_feed_data['connector'] = price_feed_connector

            if price_feed_data != {}:
                token_data['price_feed'] = price_feed_data

            db_data[ETHEREUM][token_address_eth] = token_data
    
    # POLYGON Node
    if token_address_pol != None and len(str(token_address_pol)) > 0:
        token_symbol = get_symbol(token_address_pol, POLYGON)

        try:
            token_data = db_data[POLYGON][token_address_pol]
            
            if token_address_eth != None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth
            
            if token_address_xdai != None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai
            
            token_data['symbol'] = token_symbol

            try:
                price_feed_data = db_data[POLYGON][token_address_pol]['price_feed']

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector
            
            except:
                price_feed_data = {}

                if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

                if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
                if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                    price_feed_data['connector'] = price_feed_connector

                if price_feed_data != {}:
                    db_data[POLYGON][token_address_pol]['price_feed'] = price_feed_data
        
        except:
            token_data = {}
            price_feed_data = {}

            if token_address_eth != None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth
            
            if token_address_xdai != None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai
            
            token_data['symbol'] = token_symbol

            if price_feed_source != None and len(str(price_feed_source)) > 0:
                    price_feed_data['source'] = price_feed_source

            if price_feed_blockchain != None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data['blockchain'] = price_feed_blockchain
                
            if price_feed_connector != None and len(str(price_feed_connector)) > 0:
                price_feed_data['connector'] = price_feed_connector

            if price_feed_data != {}:
                token_data['price_feed'] = price_feed_data

            db_data[POLYGON][token_address_pol] = token_data
    
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/token_mapping.json', 'w') as db_file:
        json.dump(db_data, db_file)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_lptoken_dbs
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_lptoken_dbs(protocol, lptoken_address, blockchain, **kwargs):

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/lptoken_db.json', 'r') as lptoken_db_file:
        # Reading from json file
        lptoken_db_data = json.load(lptoken_db_file)
        lptoken_db_file.close()
    
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/protocol_lptoken_db.json', 'r') as protocol_lptoken_db_file:
        # Reading from json file
        protocol_lptoken_db_data = json.load(protocol_lptoken_db_file)
        protocol_lptoken_db_file.close()
    
    web3 = get_node(ETHEREUM)

    if not web3.isChecksumAddress(lptoken_address):
        lptoken_address = web3.toChecksumAddress(lptoken_address)
    
    try:
        lptoken_db_data_item = lptoken_db_data[lptoken_address]
    except:
        lptoken_db_data_item = {}
        lptoken_db_data[lptoken_address] = lptoken_db_data_item
    
    try:
        lptoken_db_data_item_tokens = lptoken_db_data[lptoken_address]['tokens']
    except:
        lptoken_db_data_item_tokens = []
        lptoken_db_data[lptoken_address]['protocol'] = ''
        lptoken_db_data[lptoken_address]['blockchain'] = ''
        lptoken_db_data[lptoken_address]['pool_name'] = ''
        lptoken_db_data[lptoken_address]['tokens'] = lptoken_db_data_item_tokens
    
    try:
        protocol_lptoken_db_data_protocol = protocol_lptoken_db_data[protocol]
    except:
        protocol_lptoken_db_data_protocol = {}
        protocol_lptoken_db_data[protocol] = protocol_lptoken_db_data_protocol
    
    try:
        protocol_lptoken_db_data_item = protocol_lptoken_db_data_protocol[lptoken_address]
    except:
        protocol_lptoken_db_data_item = {}
        protocol_lptoken_db_data[protocol][lptoken_address] = protocol_lptoken_db_data_item
    
    try:
        protocol_lptoken_db_data_item_tokens = protocol_lptoken_db_data_protocol[lptoken_address]['tokens']
    except:
        protocol_lptoken_db_data_item_tokens = []
        protocol_lptoken_db_data[protocol][lptoken_address]['blockchain'] = ''
        protocol_lptoken_db_data[protocol][lptoken_address]['pool_name'] = ''
        protocol_lptoken_db_data[protocol][lptoken_address]['tokens'] = protocol_lptoken_db_data_item_tokens
    
    
    exec("lptoken_data="+protocol+".get_lptoken_data('%s','%s','%s')" % (lptoken_address, 'latest', blockchain), globals())

    token0_symbol = get_symbol(lptoken_data['token0'], blockchain)
    token1_symbol = get_symbol(lptoken_data['token1'], blockchain)

    # Update lptoken_db.json
    lptoken_db_data[lptoken_address]['protocol'] = protocol
    lptoken_db_data[lptoken_address]['blockchain'] = blockchain
    lptoken_db_data[lptoken_address]['pool_name'] = (protocol + ' ' + token0_symbol + '/' + token1_symbol)
    lptoken_db_data[lptoken_address]['tokens'] = [lptoken_data['token0'],lptoken_data['token1']]

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/lptoken_db.json', 'w') as lptoken_db_file:
        json.dump(lptoken_db_data, lptoken_db_file)
    
    # Update protocol_lptoken_db.json
    protocol_lptoken_db_data[protocol][lptoken_address]['blockchain'] = blockchain
    protocol_lptoken_db_data[protocol][lptoken_address]['pool_name'] = (protocol + ' ' + token0_symbol + '/' + token1_symbol)
    protocol_lptoken_db_data[protocol][lptoken_address]['tokens'] = [lptoken_data['token0'], lptoken_data['token1']]

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/protocol_lptoken_db.json', 'w') as protocol_lptoken_db_file:
        json.dump(protocol_lptoken_db_data, protocol_lptoken_db_file)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# create_txs_json
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_txs_json(from_address, signature, abi):

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0])+'/addresses.json', 'r') as addresses_file:
        # Reading from json file
        addresses = json.load(addresses_file)
        addresses_file.close()
    
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0])+'/to_addresses.json', 'r') as to_addresses_file:
        # Reading from json file
        to_addresses = json.load(to_addresses_file)
        to_addresses_file.close()
    
    web3 = get_node(ETHEREUM)

    txs = []

    from_address = web3.toChecksumAddress(from_address)

    sig_hex = web3.keccak(text = signature).hex()[2:10]
    
    for address in addresses:

        address = web3.toChecksumAddress(address)

        for to_address in to_addresses:

            to_address = web3.toChecksumAddress(to_address)

            abi_hex = eth_abi.encode_abi(abi, [to_address, 115792089237316195423570985008687907853269984665640564039457584007913129639935]).hex()

            tx = {}
            tx['from'] = from_address
            tx['to'] = to_address
            tx['data'] = '0x' + sig_hex + abi_hex

            txs.append(tx)

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0])+'/txs.json', 'w') as txs_file:
        json.dump(txs, txs_file)

# sig = Web3.keccak(text = 'approve(address,uint256)').hex()[2:10]
# abi = eth_abi.encode_abi(['address', 'uint256'], ['0xBA12222222228d8Ba445958a75a0704d566BF2C8', 115792089237316195423570985008687907853269984665640564039457584007913129639935]).hex()
# print(sig+abi)
# joinKind = 1
# minimumBPT = 8315621620078517466395
# initBalances = [4337484211030485620449, 3883468092200897599274]
# abi = ['uint256', 'uint256[]', 'uint256']
# data = [joinKind, initBalances, minimumBPT]
# userDataEncoded = eth_abi.encode_abi(abi, data)

# print(userDataEncoded.hex())

# print(int('0000000000000000000000000000000000000000000000000000000000000001', 16))
# print(int('0000000000000000000000000000000000000000000000000000000000000060', 16))
# print(int('0000000000000000000000000000000000000000000001c2ca6ead68ea54b51b', 16))
# print(int('0000000000000000000000000000000000000000000000000000000000000002', 16))
# print(int('0000000000000000000000000000000000000000000000eb22af7cf4b98fd6e1', 16))
# print(int('0000000000000000000000000000000000000000000000d285f2365c666dd72a', 16))

create_txs_json('0x849d52316331967b6ff1198e5e32a0eb168d039d', 'approve(address,uint256)', ['address', 'uint256'])