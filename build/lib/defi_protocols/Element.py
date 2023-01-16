from defi_protocols.functions import *
from defi_protocols.constants import ABI_TOKEN_SIMPLIFIED
from defi_protocols.util.topic import TopicCreator,DecodeAddressHexor
from web3 import Web3
#from defi_protocols import Curve
from defi_protocols.Curve import underlying_amount




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
ELEMENT_TRANCHE_ADDRESS = '0x17cb1f74119dfe718f786a05bea7d71bf438678c'
ELEMENT_LP_PYVCURVE = '0x07f589eA6B789249C83992dD1eD324c3b80FD06b'
ELEMENT_YVCURVE = '0xcD62f09681dCBB9fbc5bA8054B52F414Cb28960A'
BALANCER_POOL_ADDRESS = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'
ELEMENT_DEPLOYER = '0xe88628700eae9213169d715148ac5a5f47b5dcd9'

#balanceOf, interestToken, underlying
PT_ABI = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"interestToken","outputs":[{"internalType":"contract IInterestToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"underlying","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlockTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

#TotalSupply, balanceOf, getPoolID, , getVault, expiration, unitseconds, bond
#expiration - block.timestamp, *1e18, divdown by unitseconds *1e18, 
LP_PYV_ABI = '[{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"getVault","outputs":[{"internalType":"contract IVault","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"expiration","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"unitSeconds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, \
                {"inputs":[],"name":"bond","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bondDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

#getPoolTokens
BALANCER_VAULT_ABI = '[{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"}]'

#create, owner
DEPLOYER_ABI = '[{"inputs":[{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_bond","type":"address"},{"internalType":"uint256","name":"_expiration","type":"uint256"},{"internalType":"uint256","name":"_unitSeconds","type":"uint256"},{"internalType":"uint256","name":"_percentFee","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_pauser","type":"address"}],"name":"create","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},\
            {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'



def get_addresses(block, blockchain, web3=None, execution=1, index=0):
    if execution > MAX_EXECUTIONS:
        return None
    principal_tokens = []
    
    try:
        if web3 == None:
            web3 = get_node(blockchain, block=block, index=index)

        underlying_address = web3.toChecksumAddress(ELEMENT_DEPLOYER)
        tx_list = get_tx_list(contract_address=underlying_address,block_start=0,block_end=block,blockchain=blockchain)
        for i in tx_list[:-3]:
            input_data = i['input']
            deploy_contract = get_contract(underlying_address,blockchain,web3=web3,abi=DEPLOYER_ABI, block=block)
            function_output = deploy_contract.decode_function_input(input_data)
            tx = web3.eth.get_transaction_receipt(i['hash'])
            yield_token = get_contract(function_output[1]['_bond'],blockchain,web3=web3,abi=PT_ABI, block=block).functions.interestToken().call()
            pool_id = tx['logs'][0]['topics'][1].hex()
            pool_address = str(DecodeAddressHexor(tx['logs'][0]['topics'][2].hex()))
            principal_tokens.append([function_output[1]['_name'], function_output[1]['_bond'], yield_token , function_output[1]['_underlying'], pool_id, pool_address, function_output[1]['_expiration']])
        return principal_tokens
    
    
    except GetNodeIndexError:
        return get_addresses(block, blockchain, index=0, execution=execution + 1)

    except:
        return get_addresses(block, blockchain, index=index + 1, execution=execution)   


def underlying(lptoken_address, wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param reward:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 == None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.toChecksumAddress(wallet)
        token_addresses = [x for x in get_addresses(block, blockchain, web3=web3, execution=1, index=0) if x[3] == lptoken_address][0]
        pool_token_contract = get_contract(token_addresses[5],blockchain=blockchain,web3=web3,abi=LP_PYV_ABI,block=block)
        pt_token = token_addresses[1]
        pt_token_contract = get_contract(pt_token,blockchain,web3=web3,abi=PT_ABI,block=block)
        #yt_token = token_addresses[2]
        underlying_token = token_addresses[3]
        underlying_token_contract = get_contract(underlying_token,blockchain,web3=web3,abi=ABI_TOKEN_SIMPLIFIED,block=block)
        #yt_token_contract = get_contract(yt_token,blockchain,web3=web3,abi=ABI_TOKEN_SIMPLIFIED,block=block)

        pt_token_balanceOf = pt_token_contract.functions.balanceOf(wallet).call()
        #yt_token_balanceOf = yt_token_contract.functions.balanceOf(wallet).call()
        #print(yt_token_balanceOf)
        underlying_token_balanceOf = underlying_token_contract.functions.balanceOf(wallet).call()
        
        pool_total_supply = pool_token_contract.functions.totalSupply().call()
        pool_share_wallet = pool_token_contract.functions.balanceOf(wallet).call()/pool_total_supply
        pool_id = token_addresses[4]
        pool_token_vault_address = pool_token_contract.functions.getVault().call()

        pool_token_vault = get_contract(pool_token_vault_address,blockchain,web3=web3,abi=BALANCER_VAULT_ABI,block=block)
        pool_totals = pool_token_vault.functions.getPoolTokens(pool_id).call()
        amount = pt_token_balanceOf + pool_totals[1][0]*pool_share_wallet + pool_totals[1][1]*pool_share_wallet + underlying_token_balanceOf
        decimals = get_decimals(lptoken_address, blockchain, web3=web3)

        curve_amount = underlying_amount(amount/(10**decimals),underlying_token,block,blockchain,web3)
        if amount > 0:
            balances.append(curve_amount[0][:2])
            balances.append(curve_amount[1][:2])
        return balances


    except GetNodeIndexError:
        return underlying(lptoken_address,wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(lptoken_address, wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1, execution=execution)    
    



def underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param reward:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 == None:
            web3 = get_node(blockchain, block=block, index=index)

        topic0 = TopicCreator('CCPoolCreated (index_topic_1 address pool, index_topic_2 address bondToken)')
        deployed_addresses = get_logs(address=ELEMENT_DEPLOYER,block_start=0,block_end=block,blockchain=blockchain,topic0=topic0)
        for pool in deployed_addresses:
            pool_token = str(DecodeAddressHexor(pool['topics'][1]))
            balances.append(underlying(pool_token,wallet,block,blockchain))
        return balances

    except GetNodeIndexError:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1, execution=execution)    
  

    



#to test
# wallet='0x849D52316331967b6fF1198e5E32A0eB168D039d'
# lp = '0x06325440D014e39736583c165C2963BA99fAf14E'
# element = underlying(lp,wallet,'latest',blockchain=ETHEREUM)
# print(element)

# Y = 0.0468
# F = 1
# T = 2 / 12
# P = F / ((Y+1)**T)
# print(P)

# poolsteCRV = 349.1183
# poolPT = 1069.4030
# Price = 0.9919958196811649
# Total = (P*poolPT) + poolsteCRV
# Total2 = (Price*poolPT) + poolsteCRV
# print(Total)
# print(Total2)


