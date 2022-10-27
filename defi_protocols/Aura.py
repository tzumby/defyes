from general.blockchain_functions import *
from defi_protocols import Balancer

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
BOOSTER = '0x7818A1DA7BD1E64c199029E86Ba244a9798eEE10'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AURA LOCKER TOKEN ADDRESS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AURA locker token address
AURA_LOCKER = '0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster ABI - poolInfo
ABI_BOOSTER = '[{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}]'

# Rewards ABI - balanceOf, totalSupply, earned, rewardToken, extraRewardsLength, extraRewards
ABI_REWARDS = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# AURA ABI - EMISSIONS_MAX_SUPPLY, INIT_MINT_AMOUNT, decimals, reductionPerCliff, totalCliffs, totalSupply
ABI_AURA = '[{"inputs":[],"name":"EMISSIONS_MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"INIT_MINT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA LOCKER ABI - balanceOf, claimableRewards
ABI_AURA_LOCKER = '[{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"claimableRewards","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct AuraLocker.EarnedData[]","name":"userRewards","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
# Output: pool_info method return a list with the following data: 
# [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(booster_contract, lptoken_address, block):

    number_of_pools = booster_contract.functions.poolLength().call(block_identifier = block)

    for pool_id in range(number_of_pools):

        pool_info = booster_contract.functions.poolInfo(pool_id).call(block_identifier = block)
        address = pool_info[0]
        shutdown_status = pool_info[5]

        if address == lptoken_address and shutdown_status == False:
            return pool_info

    return None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_rewards
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuples: [bal_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_rewards(web3, bal_rewards_contract, wallet, block, blockchain, **kwargs):
    
    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    reward_token_address = bal_rewards_contract.functions.rewardToken().call()

    if decimals == True:
        reward_token_decimals = get_decimals(reward_token_address, blockchain, web3 = web3)
    else:
        reward_token_decimals = 0

    bal_rewards = bal_rewards_contract.functions.earned(wallet).call(block_identifier = block) / (10**reward_token_decimals)

    return [reward_token_address, bal_rewards]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_extra_rewards
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards(web3, bal_rewards_contract, wallet, block, blockchain, **kwargs):

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    extra_rewards = []

    extra_rewards_length = bal_rewards_contract.functions.extraRewardsLength().call(block_identifier = block)

    for i in range(extra_rewards_length):
        
        extra_reward_contract_address = bal_rewards_contract.functions.extraRewards(i).call(block_identifier = block)
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
# get_aura_mint_amount
# **kwargs:
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [aura_token_address, minted_amount]
# WARNING: Check the amount of AURA retrieved
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_aura_mint_amount(web3, bal_earned, block, blockchain, **kwargs):

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True

    aura_amount = 0

    aura_contract = get_contract(AURA_ETH, blockchain, web3 = web3, abi = ABI_AURA, block = block)

    aura_total_supply = aura_contract.functions.totalSupply().call(block_identifier = block)
    init_mint_amount = aura_contract.functions.INIT_MINT_AMOUNT().call(block_identifier = block)
    reduction_per_cliff = aura_contract.functions.reductionPerCliff().call(block_identifier = block)

    emissions_minted = aura_total_supply - init_mint_amount
    cliff = emissions_minted / reduction_per_cliff

    total_cliffs = aura_contract.functions.totalCliffs().call(block_identifier = block)

    if cliff < total_cliffs:

        reduction = ((total_cliffs - cliff) * 2.5) + 700

        aura_amount = (bal_earned * reduction) / total_cliffs

        amount_till_max = aura_contract.functions.EMISSIONS_MAX_SUPPLY().call(block_identifier = block) - emissions_minted
        
        if aura_amount > amount_till_max:
            aura_amount = amount_till_max
    
    if decimals == False:
        aura_decimals = get_decimals(AURA_ETH, blockchain, web3 = web3)
        aura_amount = aura_amount * (10**aura_decimals)
    
    return [AURA_ETH, aura_amount]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'bal_rewards_contract' = bal_rewards_contract -> Improves performance
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
            bal_rewards_contract = kwargs['bal_rewards_contract']
        except:
            booster_contract = get_contract(BOOSTER, blockchain, web3 = web3, abi = ABI_BOOSTER, block = block)
            pool_info = get_pool_info(booster_contract, lptoken_address, block)

            if pool_info == None:
                print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
                return None

            bal_rewards_address = pool_info[3]
            bal_rewards_contract = get_contract(bal_rewards_address, blockchain, web3 = web3, abi = ABI_REWARDS, block = block)
        
        bal_rewards = get_bal_rewards(web3, bal_rewards_contract, wallet, block, blockchain, decimals = decimals)
        all_rewards.append(bal_rewards)
        
        # all_rewards[0][1] = bal_rewards_amount - aura_mint_amount is calculated using the bal_rewards_amount
        if all_rewards[0][1] >= 0:
            aura_mint_amount = get_aura_mint_amount(web3, all_rewards[0][1], block, blockchain, decimals = decimals)
        
            if (len(aura_mint_amount) > 0):
                all_rewards.append(aura_mint_amount)

        extra_rewards = get_extra_rewards(web3, bal_rewards_contract, wallet, block, blockchain, decimals = decimals)
        
        if len(extra_rewards) > 0:
            for extra_reward in extra_rewards:
                all_rewards.append(extra_reward)
        
        aura_locked_contract = get_contract(AURA_LOCKER, blockchain, web3 = web3, block = block)
        aura_locked_rewards = aura_locked_contract.functions.claimableRewards(wallet).call(block_identifier = block)

        for aura_locked_reward in aura_locked_rewards:
            
            if aura_locked_reward[1] > 0:

                if decimals == True:
                    reward_decimals = get_decimals(aura_locked_reward[0], blockchain, web3 = web3)
                else:
                    reward_decimals = 0

                all_rewards.append([aura_locked_reward[0], aura_locked_reward[1] / (10**reward_decimals)])

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
# get_locked
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [aura_token_address, locked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_locked(wallet, block, blockchain, **kwargs):

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
        web3 = get_node(blockchain, block = block, index = index)
        
        wallet = web3.toChecksumAddress(wallet)

        aura_locked_contract = get_contract(AURA_LOCKER, blockchain, web3 = web3, block = block)

        if decimals == True:
            aura_decimals = get_decimals(AURA_ETH, blockchain, web3 = web3)
        else:
            aura_decimals = 0
        
        aura_locked = aura_locked_contract.functions.balances(wallet).call(block_identifier = block)[0] / (10**aura_decimals)

        result = [[AURA_ETH, aura_locked]]

        if reward == True:
            rewards = []
            aura_locked_rewards = aura_locked_contract.functions.claimableRewards(wallet).call(block_identifier = block)

            for aura_locked_reward in aura_locked_rewards:

                if aura_locked_reward[1] > 0:

                    if decimals == True:
                        reward_decimals = get_decimals(aura_locked_reward[0], blockchain, web3 = web3)
                    else:
                        reward_decimals = 0

                    rewards.append([aura_locked_reward[0], aura_locked_reward[1] / (10**reward_decimals)])
            
            result += rewards

        return result
        
    except GetNodeLatestIndexError:
        index = 0

        return get_locked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0

        return get_locked(wallet, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
    except Exception as Ex:
        traceback.print_exc()
        return get_locked(wallet, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'no_balancer_underlying' = True -> retrieves the LP Token balance / 
# 'no_balancer_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Balancer tokens
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_balancer_underlying' value 
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
        no_balancer_underlying = kwargs['no_balancer_underlying']
    except:
        no_balancer_underlying = False

    try:
        decimals = kwargs['decimals']
    except:
        decimals = True
    
    result = []
    balances = []
    
    try:
        web3 = get_node(blockchain, block = block, index = index)

        wallet = web3.toChecksumAddress(wallet)
        
        lptoken_address = web3.toChecksumAddress(lptoken_address)
        
        booster_contract = get_contract(BOOSTER, blockchain, web3 = web3, abi = ABI_BOOSTER, block = block)

        pool_info = get_pool_info(booster_contract, lptoken_address, block)

        if pool_info == None:
            print('Error: Incorrect Aura LPToken Address: ', lptoken_address)
            return None
        
        bal_rewards_address = pool_info[3]
        bal_rewards_contract = get_contract(bal_rewards_address, blockchain, web3 = web3, abi = ABI_REWARDS, block = block)

        lptoken_staked = bal_rewards_contract.functions.balanceOf(wallet).call(block_identifier = block)

        if no_balancer_underlying == False:
            balancer_data = Balancer.underlying(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, aura_staked = lptoken_staked, index = index)
            balances = [[balancer_data[i][0], balancer_data[i][2]] for i in range(len(balancer_data))]
        else:
            if decimals == True:
                lptoken_decimals = get_decimals(lptoken_address, blockchain, web3 = web3)
            else:
                lptoken_decimals = 0
            
            lptoken_staked = lptoken_staked / (10**lptoken_decimals)

            balances.append([lptoken_address, lptoken_staked])

        if reward == True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, bal_rewards_contract = bal_rewards_contract, index = index)
            
            result.append(balances)
            result.append(all_rewards)
        
        else:
            result = balances

        return result
    
    except GetNodeLatestIndexError:
        index = 0

        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, no_balancer_underlying = no_balancer_underlying, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0
        
        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, no_balancer_underlying = no_balancer_underlying, index = index, execution = execution + 1)

    except Exception as Ex:
        traceback.print_exc()
        return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, no_balancer_underlying = no_balancer_underlying, index = index + 1, execution = execution)
    
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

        balances = Balancer.pool_balances(lptoken_address, block, blockchain, web3 = web3, decimals = decimals, index = index)

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