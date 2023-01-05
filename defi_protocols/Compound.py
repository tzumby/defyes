from defi_protocols.functions import *
from defi_protocols.constants import *
from time import sleep
from rich.progress import track


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COMPOUND CONTROLLER ADDRESS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
COMPOUND_CONTROLLER_ADDRESS = ' '
COMPOUND_TOKEN = '0xc00e94Cb662C3520282E6f5717214004A7f26888'

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABI CONTRACT ADDRESS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ABI_CONTRACT_ADDRESS = '0xbafe01ff935c7305907c33bf824352ee5979b526'

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

    token_data = {}

    token_data['contract']  = get_contract(contract_address=token_address, blockchain=blockchain, abi=abi)

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


def underlying(wallet, token_address, block, blockchain, web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None):
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
    # try:
    web3 = get_node(blockchain, block=block, index=index)
    compound_controller_add = web3.toChecksumAddress(COMPOUND_CONTROLLER_ADDRESS)
    controller_contract = get_contract_proxy_abi(compound_controller_add,ABI_CONTRACT_ADDRESS, blockchain)

    index=0

    if web3 is None:
            web3 = get_node('ethereum', block=block, index=0)

    wallet = web3.toChecksumAddress(wallet)

    token_address = web3.toChecksumAddress(token_address)

    if c_token_list == None or underlying_token_list == None :
        c_token_list = controller_contract.functions.getAllMarkets().call()

        underlying_token_list = []
        
        for c_token in track(c_token_list, description="Downloading Compound Token list..."):
            
            underlying_token_data  = get_contract(contract_address=c_token, blockchain=blockchain)
            try:
                o_tk = underlying_token_data.functions.underlying().call()
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
    

    c_token_data['borrowBalanceStored'] = c_token_data['borrowBalanceStored']/10**c_token_data['decimals']  or 0
        
    
    
    exchange_rate = c_token_data['contract'].functions.exchangeRateStored().call()


    try:
        underlying_token_decimals = get_decimals(token_address, block, blockchain, web3=web3, index=index)
    except:

        underlying_token_decimals = 18
        
    mantissa = 18 + int(c_token_data['decimals']) - int(underlying_token_decimals)

    oneCTokenInUnderlying = exchange_rate / 10**mantissa


    underlying_token_balance = ((c_token_data['balanceOf']) * oneCTokenInUnderlying)/(10**(18 - int(c_token_data['decimals']) + int(underlying_token_decimals))) - c_token_data['borrowBalanceStored']
    


    underlying_token_balance = underlying_token_balance


    return token_address, underlying_token_balance
    
    # except GetNodeIndexError:
      
    #     return underlying(wallet, block, blockchain,  index=0, execution=execution + 1)

    # except:
     
    #     return underlying(wallet, block, blockchain, index=index + 1, execution=execution)


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
    print('hola')
    print(assets_c_token_list)
    # Transform c token to underlying tokens:ç

    for c_token in track(assets_c_token_list, description="Checking Compound Token list..."):
        
        token_data  = get_contract(contract_address=c_token, blockchain=blockchain)
        print('the token data',token_data)
        try:
            o_tk = token_data.functions.underlying().call()
            # print (c_token,o_tk)
            underlying_token_list.append(o_tk)
        except:
            print(underlying_token_list)
            underlying_token_list.append('0x0000000000000000000000000000000000000000') #es asi?


    balance_tokens = []
    token_ref_list = [assets_c_token_list,underlying_token_list]
    print(underlying_token_list)
    
    for underlying_token in underlying_token_list:
        underlying_return = underlying(wallet=wallet, token_address=underlying_token, block=block, blockchain=blockchain, web3=None, execution=1, index=0, c_token_list = assets_c_token_list, underlying_token_list=underlying_token_list)
        
        balance_tokens.append(underlying_return)


    return balance_tokens



''' 
----- Testing -----
'''



# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# j=underlying_all(wallet, 'latest', 'ethereum')
# print ('wallet1',j)

# wallet = '0x716034C25D9Fb4b38c837aFe417B7f2b9af3E9AE'
# j=underlying_all(wallet, 'latest', 'ethereum')
# print ('wallet2',j)



# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# j=underlying_all(wallet, 'latest', 'ethereum')
# print ('wallet1',j)

# J=underlying(wallet, token_address='0x6B175474E89094C44Da98b954EedeAC495271d0F', block='latest', blockchain='ethereum', web3=None, execution=1, index=0, c_token_list = None, underlying_token_list=None)
# print (J)