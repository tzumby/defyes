from defi_protocols.functions import *

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
BANCOR_NETWORK_ADDRESS = '0xeEF417e1D5CC832e619ae18D2F140De2999dD4fB'

BANCOR_NETWORK_INFO_ADDRESS = '0x8E303D296851B320e6a697bAcB979d13c9D6E760'


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Network ABI - liquidityPools
ABI_NETWORK = '[{"inputs":[],"name":"liquidityPools","outputs":[{"internalType":"contract Token[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"}]'

# NetworkInfo ABI - poolToken, withdrawalAmounts
ABI_NETWORK_INFO = '[{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"}],"name":"poolToken","outputs":[{"internalType":"contract IPoolToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"},{"internalType":"uint256","name":"poolTokenAmount","type":"uint256"}],"name":"withdrawalAmounts","outputs":[{"components":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"uint256","name":"baseTokenAmount","type":"uint256"},{"internalType":"uint256","name":"bntAmount","type":"uint256"}],"internalType":"struct WithdrawalAmounts","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]'

# ABI of the pools - balanceOf, reserveToken
ABI_POOL = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveToken","outputs":[{"internalType":"contract Token","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


def underlying(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
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
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.toChecksumAddress(wallet)

    #get the bancornetwork contract to call function for all liquiditypools
        liquiditypools_contract = get_contract(BANCOR_NETWORK_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK, block=block)
    #call function for all liquiditypools
        liquidity_pools = liquiditypools_contract.functions.liquidityPools().call()
    #get the bancornetworkinfo contract so we can get all bnToken pool addresses
        pooltoken_contract = get_contract(BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO, block=block)
    #make list for amounts
        
    #print('all pools are: ',liquidityPools)
        for pool in liquidity_pools:
        #for each address, get the bancor pool address
            bancor_pool = pooltoken_contract.functions.poolToken(pool).call()

            bancor_poolcontract=get_contract(bancor_pool, blockchain, web3=web3, abi=ABI_POOL, block=block)
        #call the balanceOf function
        #print(bancorPoolContract)
            balance = bancor_poolcontract.functions.balanceOf(wallet).call(block_identifier=block)
        #when no balance in the pool go to next one
            if balance == 0:
                continue
        #when balance append pooladdress and balance to list
            else:
                balances.append([bancor_pool,balance])
            #print('tokens in pool: ',balance, ' ', symbol)
        return balances

    except GetNodeIndexError:
        return underlying(wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1, execution=execution)

#calculate IP
def impermanentLoss(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    tokenAmounts = underlying(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True)
    print('amounts for wallet are: ',tokenAmounts)
    impermanentLossAmounts = []
    for token in tokenAmounts:
        #get the poolcontract to call function balanceOf
        #print(bancorPoolABI)
        bancorPoolContract=get_contract(token[0], blockchain, web3=web3, abi=ABI_POOL, block=block)
        #call the balanceOf function
        #print(bancorPoolContract)
        reserveToken = bancorPoolContract.functions.reserveToken().call()
        #get ABI for bancor networkinfo contract
        poolTokenscontract = get_contract(BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO, block=block)
        #for each address, get the bancor pool address
        bancorPool = poolTokenscontract.functions.withdrawalAmounts(reserveToken,token[1]).call()
        impermanentLossAmounts.append(bancorPool)
    return impermanentLossAmounts
        

#to test
#wallet='0x849d52316331967b6ff1198e5e32a0eb168d039d'
#bancor = underlying(wallet,'latest',ETHEREUM)
#print(bancor)
