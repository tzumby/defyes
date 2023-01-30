from defi_protocols.functions import *
from defi_protocols.constants import *
from time import sleep
from tqdm import *


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COMPOUND CONTROLLER ADDRESS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
COMPOUND_CONTROLLER_ADDRESS = '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B'
COMPOUND_TOKEN = '0xc00e94Cb662C3520282E6f5717214004A7f26888'
COMPOUND_API_CONTRACT = '0xdCbDb7306c6Ff46f77B349188dC18cEd9DF30299'

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABI CONTRACT ADDRESS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ABI_CONTRACT_ADDRESS = '0xbafe01ff935c7305907c33bf824352ee5979b526'


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# WEB DOCS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
https://docs.compound.finance/v2/
'''





''' ------------------------------'''
''' ------- GET TOKEN DATA -------'''
''' ------------------------------'''

def get_token_data(token_address, block, blockchain, abi=None,web3=None, index=0):
    if web3 is None:
        web3 = get_node('ethereum', block=block, index=0)

    token_data = {}

    token_data['contract']  = get_contract(contract_address=token_address, blockchain=blockchain, abi=abi,web3=web3)

    try:
        token_data['decimals'] = token_data['contract'].functions.decimals().call()
        
    except:
        token_data['decimals'] = None
    try:
        token_data['totalSupply'] = token_data['contract'].functions.totalSupply().call(block_identifier=block)
    except:
        token_data['totalSupply'] = None
    
    return token_data


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'c_token_list' and 'underlying_token_list' = specifies if there is a tocken/c_token reference list provided or not. If None it would get the reference list from the smart contract
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance], where balance = currentATokenBalance 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def underlying(wallet, token_address, block, blockchain, web3=None,decimals=True, execution=1, index=0, c_token_list = None, underlying_token_list=None):
    """

    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param c_token_list:
    :param underlying_token_list:
    :return:
    """
    
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None
    
    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)
        compound_controller_add = web3.toChecksumAddress(COMPOUND_CONTROLLER_ADDRESS)
        controller_contract = get_contract_proxy_abi(compound_controller_add,ABI_CONTRACT_ADDRESS, blockchain, web3=web3,block=block)

        

        

        wallet = web3.toChecksumAddress(wallet)

        token_address = web3.toChecksumAddress(token_address)

        if c_token_list == None or underlying_token_list == None :
            c_token_list = controller_contract.functions.getAllMarkets().call()

            underlying_token_list = []
            
            for c_token in tqdm(c_token_list,desc="Loading Token Data"):
                
                underlying_token_data  = get_contract(contract_address=c_token, blockchain=blockchain)
                try:
                    o_tk = underlying_token_data.functions.underlying().call(block_identifier=block)
                    # print (c_token,o_tk)
                    underlying_token_list.append(o_tk)
                except:
                    underlying_token_list.append('0x0000000000000000000000000000000000000000') 


        
        underlying_token_index = underlying_token_list.index(token_address)
        c_token = c_token_list[underlying_token_index]
        

        c_token_data = get_token_data(c_token, block, blockchain, web3=web3, index=index)
        #balance of underlying token
        c_token_data['balanceOf'] = c_token_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)
        
        c_token_data['borrowBalanceStored'] = c_token_data['contract'].functions.borrowBalanceStored(wallet).call(block_identifier=block)
        
        c_token_data['decimals'] = c_token_data['contract'].functions.decimals().call(block_identifier=block)
        
        if decimals == True:
        #divide by decimals 
             c_token_data['borrowBalanceStored'] = c_token_data['borrowBalanceStored']/10**c_token_data['decimals']  or 0
             c_token_data['balanceOf'] = c_token_data['balanceOf']/10**c_token_data['decimals']  or 0
            
      
        
        
        exchange_rate = c_token_data['contract'].functions.exchangeRateStored().call(block_identifier=block)
        # print('ex_rate', exchange_rate)


        # try:
        underlying_token_decimals = get_decimals(token_address, block=block, blockchain=blockchain, web3=web3, index=index)
        # except:

        #     underlying_token_decimals = 18
            
        mantissa = 18 - (c_token_data['decimals']) + int(underlying_token_decimals)

        oneCTokenInUnderlying = exchange_rate / (10**mantissa)


        underlying_token_balance = ((c_token_data['balanceOf']) * oneCTokenInUnderlying) - c_token_data['borrowBalanceStored']*oneCTokenInUnderlying
        


        underlying_token_balance = underlying_token_balance
        balance = [token_address, underlying_token_balance]
        #to return same format as others protocols 
        balances = [balance]
        return balances
    
    except GetNodeIndexError:
      
         return underlying(wallet, block, blockchain,  index=0, execution=execution + 1)

    except:
     
         return underlying(wallet, block, blockchain, index=index + 1, execution=execution)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance], where balance = currentATokenBalance  
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
    
    web3 = get_node(blockchain, block=block, index=index)
    compound_controller_add = web3.toChecksumAddress(COMPOUND_CONTROLLER_ADDRESS)

    wallet=web3.toChecksumAddress(wallet)

    controller_contract = get_contract_proxy_abi(compound_controller_add,ABI_CONTRACT_ADDRESS, blockchain)
    #get c_tokens
    assets_c_token_list = controller_contract.functions.getAssetsIn(wallet).call()



    underlying_token_list = []
  
    print(assets_c_token_list)
    # Transform c token to underlying tokens:ç

    for c_token in assets_c_token_list:
        
        token_data  = get_contract(contract_address=c_token, blockchain=blockchain)
        print('the token data',token_data)
        try:
            o_tk = token_data.functions.underlying().call()
            # print (c_token,o_tk)
            underlying_token_list.append(o_tk)
        except:
            print(underlying_token_list)
            underlying_token_list.append('0x0000000000000000000000000000000000000000')


    balance_tokens = []
    token_ref_list = [assets_c_token_list,underlying_token_list]
    print(underlying_token_list)
    
    for underlying_token in underlying_token_list:
        underlying_return = underlying(wallet=wallet, token_address=underlying_token, block=block, blockchain=blockchain, web3=None, execution=1, index=0, c_token_list = assets_c_token_list, underlying_token_list=underlying_token_list)
        
        balance_tokens.append(underlying_return)


    return balance_tokens








#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'gauge_address' = gauge_address -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_all_rewards(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    
    '''
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    '''
    
    
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)
        
        wallet = web3.toChecksumAddress(wallet)    
        compound_controller_add = web3.toChecksumAddress(COMPOUND_CONTROLLER_ADDRESS)
        api_contract = web3.toChecksumAddress(COMPOUND_API_CONTRACT)
        compound_token_add = web3.toChecksumAddress(COMPOUND_TOKEN)
        
        controller_contract = get_contract(api_contract, blockchain)
        meta_data = controller_contract.functions.getCompBalanceMetadataExt(compound_token_add,compound_controller_add, wallet ).call(block_identifier=block)
        rewards = meta_data[3]
        
        compound_token_contract = get_contract(compound_token_add, blockchain)
        compound_decimals = compound_token_contract.functions.decimals().call()
        
        if decimals == True:
            rewards = meta_data[3] / 10**compound_decimals 
        
        reward = [compound_token_add, rewards]
        rewards = [reward]
        return rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet,  block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, block, blockchain,  decimals=decimals, index=index + 1, execution=execution)




''' 
----- Testing -----
'''

# dai = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
# input_date ='2023-01-10 00:00:00'
# now=datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
# block = date_to_block(now.strftime('%Y-%m-%d %H:%M:%S'),blockchain='ethereum')

# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# j=underlying(wallet,dai, 'latest', 'ethereum')
# print ('wallet',j)


# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# j2=underlying(wallet,dai, block, 'ethereum')
# print ('wallet',j2)

# wallet = '0x716034C25D9Fb4b38c837aFe417B7f2b9af3E9AE'
# j=underlying_all(wallet, 'latest', 'ethereum')
# print ('wallet2',j)



# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# # j=underlying_all(wallet, 'latest', 'ethereum')
# # print ('wallet1',j)

# J=underlying(wallet, token_address='0x6B175474E89094C44Da98b954EedeAC495271d0F', block='latest', blockchain='ethereum', web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None)
# print (J)

# j = get_all_rewards('0x849d52316331967b6ff1198e5e32a0eb168d039d', 'latest', 'ethereum')
# print(j)

# '''decimals testing:'''

# wallet = '0x4971dd016127f390a3ef6b956ff944d0e2e1e462'
# dai='0x6B175474E89094C44Da98b954EedeAC495271d0F'
# usdc='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
# j=underlying(wallet, usdc, 'latest', 'ethereum', web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None)
# print(j)
# print("{:,.0f}".format(j[0][1]))

# wallet = '0x4971dd016127f390a3ef6b956ff944d0e2e1e462'
# dai='0x6B175474E89094C44Da98b954EedeAC495271d0F'
# usdc='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
# k=underlying(wallet, dai, 'latest', blockchain='ethereum', web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None)
# print(k)
# print("{:,.0f}".format(k[0][1]))


# wallet = '0x4d7b618fbadf32c3726082b67b8f68b75cc8c6cc'
# dai='0x6B175474E89094C44Da98b954EedeAC495271d0F'
# usdc='0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
# uni = '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984'
# k=underlying(wallet, uni, 'latest', blockchain='ethereum', web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None)
# print(k)
# print("{:,.0f}".format(k[0][1]))