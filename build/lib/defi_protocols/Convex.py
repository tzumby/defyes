from general.blockchain_functions import *
from defi_protocols import Curve
from pathlib import Path
import os

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BACKLOG LIST
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rewards when you stake CVX

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
BOOSTER = '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX REWARDS TOKEN ADDRESS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX rewards token address
CVX_STAKER = '0xCF50b810E57Ac33B91dCF525C6ddd9881B139332'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX LOCKER TOKEN ADDRESS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX locker token address
CVX_LOCKER = '0x72a19342e8F1838460eBFCCEf09F6585e32db86E'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster ABI - poolInfo
ABI_BOOSTER = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}]'

# Rewards ABI - balanceOf, totalSupply, earned, rewardToken, extraRewardsLength, extraRewards
ABI_REWARDS = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# CVX ABI - reductionPerCliff, totalCliffs, maxSupply, totalSupply
ABI_CVX = '[{"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
# Output: pool_info method return a list with the following data: 
# [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(lptoken_address, block):


    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/convex.json', 'r') as db_file:
        # Reading from json file
        db_data = json.load(db_file)
    
    try:
        pool_info = db_data['pools'][lptoken_address]
        return [lptoken_address, pool_info['token'], pool_info['gauge'], pool_info['crvRewards']]
    
    except:
        booster_contract = get_contract(BOOSTER, ETHEREUM, abi = ABI_BOOSTER, block = block)

        address = None
        pool_id = -1

        while address != lptoken_address:

            pool_id = pool_id + 1

            try:
                pool_info = booster_contract.functions.poolInfo(pool_id).call()
                address = pool_info[0]
            
                if address == lptoken_address:
                    return pool_info
        
            except:
                return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_crv_rewards
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuples: [crv_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_crv_rewards(web3, crv_rewards_contract, wallet, block, blockchain, **kwargs):

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    reward_token_address = crv_rewards_contract.functions.rewardToken().call()

    if decimals == True:
        reward_token_decimals = get_decimals(reward_token_address, blockchain, web3 = web3)
    else:
        reward_token_decimals = 0

    crv_rewards = crv_rewards_contract.functions.earned(wallet).call(block_identifier = block) / (10**reward_token_decimals)

    return [reward_token_address, crv_rewards]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_extra_rewards
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, **kwargs):

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    extra_rewards = []

    extra_rewards_length = crv_rewards_contract.functions.extraRewardsLength().call(block_identifier = block)

    for i in range(extra_rewards_length):
        
        extra_reward_contract_address = crv_rewards_contract.functions.extraRewards(i).call(block_identifier = block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain, web3 = web3, abi = ABI_REWARDS, block = block)

        extra_reward_token_address = extra_reward_contract.functions.rewardToken().call()
        
        if decimals == True:
            extra_reward_token_decimals = get_decimals(extra_reward_token_address, blockchain, web3 = web3)
        else:
            extra_reward_token_decimals = 0

        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier = block) / (10**extra_reward_token_decimals)

        extra_rewards.append([extra_reward_token_address, extra_reward])
    
    return extra_rewards

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cvx_mint_amount
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [cvx_token_address, minted_amount]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cvx_mint_amount(web3, crv_earned, block, blockchain, **kwargs):

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    cvx_contract = get_contract(CVX_ETH, blockchain, web3 = web3, abi = ABI_CVX, block = block)

    cliff_size = cvx_contract.functions.reductionPerCliff().call(block_identifier = block)
    cliff_count = cvx_contract.functions.totalCliffs().call(block_identifier = block)
    max_supply = cvx_contract.functions.maxSupply().call(block_identifier = block)

    cvx_total_supply = cvx_contract.functions.totalSupply().call(block_identifier = block)

    current_cliff = cvx_total_supply / cliff_size

    if(current_cliff < cliff_count ):

        remaining = cliff_count - current_cliff
        cvx_earned = crv_earned * remaining / cliff_count
        amount_till_max = max_supply - cvx_total_supply

        if(cvx_earned > amount_till_max):
            cvx_earned = amount_till_max
    
    return [CVX_ETH, cvx_earned]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'crv_rewards_contract' = crv_rewards_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, **kwargs):

    try:
        execution = kwargs['execution']
    except:
        execution = 1

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts   
    if execution > MAX_EXECUTIONS:
        return None

    try:
        index = kwargs['index']
    except:
        index = 0
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    try:
        web3 = kwargs['web3']
    except:
        web3 = None
    
    all_rewards = []
    
    try:
        if web3 == None: 
            web3 = get_node(blockchain, block = block, index = index)
    
        wallet = web3.toChecksumAddress(wallet)
        
        lptoken_address = web3.toChecksumAddress(lptoken_address)
        
        try:
            crv_rewards_contract = kwargs['crv_rewards_contract']
        except:
            pool_info = get_pool_info(lptoken_address, block)

            if pool_info == None:
                print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
                return None

            crv_rewards_address = pool_info[3]
            crv_rewards_contract = get_contract(crv_rewards_address, blockchain, web3 = web3, abi = ABI_REWARDS, block = block)    
        
        crv_rewards = get_crv_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals = decimals)
        all_rewards.append(crv_rewards)
        
        # all_rewards[0][1] = crv_rewards_amount - cvx_mint_amount is calculated using the crv_rewards_amount
        if all_rewards[0][1] >= 0:
            cvx_mint_amount = get_cvx_mint_amount(web3, all_rewards[0][1], block, blockchain, decimals = decimals)
        
            if (len(cvx_mint_amount) > 0):
                all_rewards.append(cvx_mint_amount)

        extra_rewards = get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals = decimals)
        
        if len(extra_rewards) > 0:
            for extra_reward in extra_rewards:
                all_rewards.append(extra_reward)
        
        cvx_locked_contract = get_contract(CVX_LOCKER, blockchain, web3 = web3, block = block)
        cvx_locked_rewards = cvx_locked_contract.functions.claimableRewards(wallet).call(block_identifier = block)
        
        for cvx_locked_reward in cvx_locked_rewards:
            
            if cvx_locked_reward[1] > 0:

                if decimals == True:
                    reward_decimals = get_decimals(cvx_locked_reward[0], blockchain, web3 = web3)
                else:
                    reward_decimals = 0
            
                all_rewards.append([cvx_locked_reward[0], cvx_locked_reward[1] / (10**reward_decimals)])

        return all_rewards
    
    except GetNodeLatestIndexError:
        index = 0

        return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0

        return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except Exception as Ex:
        traceback.print_exc()
        return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cvx_locked
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [cvx_token_address, locked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cvx_locked(wallet, block, blockchain, **kwargs):

    try:
        execution = kwargs['execution']
    except:
        execution = 1

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts   
    if execution > MAX_EXECUTIONS:
        return None
    
    try:
        index = kwargs['index']
    except:
        index = 0

    try:
        reward = kwargs['reward']
    except:
        reward = False
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    result = []
    
    try:
        web3 = get_node(blockchain, block = block, index = index)
        
        wallet = web3.toChecksumAddress(wallet)

        cvx_locked_contract = get_contract(CVX_LOCKER, blockchain, web3 = web3, block = block)

        if decimals == True:
            cvx_decimals = get_decimals(CVX_ETH, blockchain, web3 = web3)
        else:
            cvx_decimals = 0
        
        cvx_locked = cvx_locked_contract.functions.balances(wallet).call(block_identifier = block)[0] / (10**cvx_decimals)

        result = [[CVX_ETH, cvx_locked]]

        if reward == True:
            rewards = []
            cvx_locked_rewards = cvx_locked_contract.functions.claimableRewards(wallet).call(block_identifier = block)

            for cvx_locked_reward in cvx_locked_rewards:
                
                if cvx_locked_reward[1] > 0:

                    if decimals == True:
                        reward_decimals = get_decimals(cvx_locked_reward[0], blockchain, web3 = web3)
                    else:
                        reward_decimals = 0
                
                    rewards.append([cvx_locked_reward[0], cvx_locked_reward[1] / (10**reward_decimals)])
            
            result += rewards

        return result
    
    except GetNodeLatestIndexError:
        index = 0

        return get_cvx_locked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0

        return get_cvx_locked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except Exception as Ex:
        traceback.print_exc()
        return get_cvx_locked(wallet, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cvx_staked
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [cvx_token_address, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cvx_staked(wallet, block, blockchain, **kwargs):

    try:
        execution = kwargs['execution']
    except:
        execution = 1

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        index = kwargs['index']
    except:
        index = 0

    try:
        reward = kwargs['reward']
    except:
        reward = False

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    result = []

    try:
        web3 = get_node(blockchain, block = block, index = index)

        wallet = web3.toChecksumAddress(wallet)

        cvx_staking_contract = get_contract(CVX_STAKER, blockchain, web3 = web3, block = block)

        if decimals == True:
            cvx_decimals = get_decimals(CVX_ETH, blockchain, web3 = web3)
        else:
            cvx_decimals = 0

        cvx_staked = cvx_staking_contract.functions.balanceOf(wallet).call(block_identifier = block) / (10 ** cvx_decimals)

        result = [[CVX_ETH, cvx_staked]]

        if reward == True:
            rewards = []
            cvx_staked_rewards = cvx_staking_contract.functions.earned(wallet).call(block_identifier = block)

            if cvx_staked_rewards > 0:

                if decimals == True:

                    reward_decimals = get_decimals(CVXCRV_ETH, blockchain, web3 = web3)

                else:
                    reward_decimals = 0

            rewards.append([CVXCRV_ETH, cvx_staked_rewards / (10 ** reward_decimals)])
            
            result += rewards

        return result

    except GetNodeLatestIndexError:
        index = 0

        return get_cvx_staked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

    except GetNodeArchivalIndexError:
        index = 0

        return get_cvx_staked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

    except Exception as Ex:
        traceback.print_exc()
        return get_cvx_staked(wallet, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'no_curve_underlying' = True -> retrieves the LP Token balance / 
# 'no_curve_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Curve tokens
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value 
# 2 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, **kwargs):

    try:
        execution = kwargs['execution']
    except:
        execution = 1

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None
    
    try:
        index = kwargs['index']
    except:
        index = 0

    try:
        reward = kwargs['reward']
    except:
        reward = False
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    try:
        no_curve_underlying = kwargs['no_curve_underlying']
    except:
        no_curve_underlying = False
    
    result = []
    balances = []
    
    try:
        web3 = get_node(blockchain, block = block, index = index)

        wallet = web3.toChecksumAddress(wallet)
        
        lptoken_address = web3.toChecksumAddress(lptoken_address)

        pool_info = get_pool_info(lptoken_address, block)

        if pool_info == None:
            print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
            return None
        
        crv_rewards_address = pool_info[3]
        crv_rewards_contract = get_contract(crv_rewards_address, blockchain, web3 = web3, abi = ABI_REWARDS, block = block)
        
        lptoken_staked = crv_rewards_contract.functions.balanceOf(wallet).call(block_identifier = block)

        if no_curve_underlying == False:
            balances = Curve.underlying(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, index = index, convex_staked = lptoken_staked)  
        else:
            if decimals == True:
                lptoken_decimals = get_decimals(lptoken_address, blockchain, web3 = web3)
            else:
                lptoken_decimals = 0
            
            lptoken_staked = lptoken_staked / (10**lptoken_decimals)

            balances.append([lptoken_address, lptoken_staked])

        if reward == True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, crv_rewards_contract = crv_rewards_contract, index = index)
            
            result.append(balances)
            result.append(all_rewards)
        
        else:
            result = balances

        return result
    
    except GetNodeLatestIndexError:
        index = 0

        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, no_curve_underlying = no_curve_underlying, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0
        
        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals,  no_curve_underlying = no_curve_underlying, index = index, execution = execution + 1)

    except Exception as Ex:
        traceback.print_exc()
        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals,  no_curve_underlying = no_curve_underlying, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, **kwargs):

    try:
        execution = kwargs['execution']
    except:
        execution = 1

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        index = kwargs['index']
    except:
        index = 0
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    balances = []
    
    try:
        web3 = get_node(blockchain, block = block, index = index)
        
        lptoken_address = web3.toChecksumAddress(lptoken_address)

        balances = Curve.pool_balances(lptoken_address, block, blockchain, web3 = web3, decimals = decimals, index = index)

        return balances
    
    except GetNodeLatestIndexError:
        index = 0

        return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0
        
        return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

    except Exception as Ex:
        traceback.print_exc()
        return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db():

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/convex.json', 'r') as db_file:
        # Reading from json file
        db_data = json.load(db_file)
    
    web3 = get_node(ETHEREUM)

    booster = get_contract(BOOSTER, ETHEREUM, web3 = web3)
    db_pool_length = len(db_data['pools'])
    pools_delta = booster.functions.poolLength().call(block_identifier = 'latest') - db_pool_length
    
    if pools_delta > 0:
        
        for i in range(pools_delta):
            pool_info = booster.functions.poolInfo(db_pool_length + i).call()
            db_data['pools'][pool_info[0]] = {
                'poolId': db_pool_length + i,
                'token': pool_info[1],
                'gauge': pool_info[2],
                'crvRewards': pool_info[3]
            }

        with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/convex.json', 'w') as db_file:
            json.dump(db_data, db_file)
