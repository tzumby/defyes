# from general.blockchain_functions import *
# from price_feeds import Prices
# from pathlib import Path
# import os


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # MASTERCHEF_V1
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # MASTERCHEF_V1 Contract Address
# MASTERCHEF_V1 = '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # MASTERCHEF_V2
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # MASTERCHEF_V2 Contract Address
# MASTERCHEF_V2 = '0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # LIQUIDITY MINING
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Polygon - MiniChef Contract Address
# MINICHEF_POLYGON = '0x0769fd68dFb93167989C6f7254cd0D766Fb2841F'

# # xDAI - MiniChef Contract Address
# MINICHEF_XDAI = '0xdDCbf776dF3dE60163066A5ddDF2277cB445E0F3'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # ABIs
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Chefs V2 ABI - SUSHI, rewarder, pendingSushi, lpToken, userInfo, poolLength, poolInfo, sushiPerBlock, sushiPerSecond, totalAllocPoint
# ABI_CHEF_V2 = '[{"inputs":[],"name":"SUSHI","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewarder","outputs":[{"internalType":"contract IRewarder","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingSushi","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lpToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint128","name":"accSushiPerShare","type":"uint128"},{"internalType":"uint64","name":"lastRewardBlock","type":"uint64"},{"internalType":"uint64","name":"allocPoint","type":"uint64"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"sushiPerBlock","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"sushiPerSecond","inputs":[]}, {"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# # Chefs V1 ABI - sushi, rewarder, pendingSushi, poolInfo, userInfo, poolLength, sushiPerBlock, totalAllocPoint
# ABI_CHEF_V1 = '[{"inputs":[],"name":"sushi","outputs":[{"internalType":"contract SushiToken","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewarder","outputs":[{"internalType":"contract IRewarder","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingSushi","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accSushiPerShare","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"sushiPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# # Rewarder ABI - pendingTokens, rewardPerSecond, poolInfo
# ABI_REWARDER = '[{"inputs":[{"internalType":"uint256","name":"pid","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"pendingTokens","outputs":[{"internalType":"contract IERC20[]","name":"rewardTokens","type":"address[]"},{"internalType":"uint256[]","name":"rewardAmounts","type":"uint256[]"}],"stateMutability":"view","type":"function"}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"rewardPerSecond","inputs":[]}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint128","name":"accSushiPerShare","type":"uint128"},{"internalType":"uint64","name":"lastRewardBlock","type":"uint64"},{"internalType":"uint64","name":"allocPoint","type":"uint64"}],"stateMutability":"view","type":"function"}]'

# # LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast
# ABI_LPTOKEN = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # EVENT SIGNATURES
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Swap Event Signature
# SWAP_EVENT_SIGNATURE = 'Swap(address,uint256,uint256,uint256,uint256,address)'

# # Deposit Event Signature
# DEPOSIT_EVENT_SIGNATURE = 'deposit(uint256,uint256,address)'


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_chef_contract
# # **kwargs: 
# # 'v1' = True -> If blockchain = ETHEREUM retrieves the MASTERCHEF_V1 Contract / 'v1' = False or not passed onto the function -> retrieves the MASTERCHEF_V2 Contract
# # Output: chef_contract
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_chef_contract(web3, block, blockchain, **kwargs):

#     # try: If kwargs['v1'] is passed onto the function or not
#     try:
#         v1 = kwargs['v1']
#     except:
#     # If kwargs['v1'] is not passed onto the function then v1 = False
#         v1 = False

#     if blockchain == ETHEREUM:
#         if v1 == False:
#             chef_contract = get_contract(MASTERCHEF_V2, blockchain, web3 = web3, abi = ABI_CHEF_V2, block = block)
#         else:
#             chef_contract = get_contract(MASTERCHEF_V1, blockchain, web3 = web3, abi = ABI_CHEF_V1, block = block)
    
#     elif blockchain == POLYGON:
#         chef_contract = get_contract(MINICHEF_POLYGON, blockchain, web3 = web3, abi = ABI_CHEF_V2, block = block)
    
#     elif blockchain == XDAI:
#         chef_contract = get_contract(MINICHEF_XDAI, blockchain, web3 = web3, abi = ABI_CHEF_V2, block = block)

#     return chef_contract

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_pool_info
# # Output:
# # 1 - Dictionary: result['chef_contract'] = chef_contract
# #                 result['pool_info'] = {
# #                     'poolId': poolID
# #                     'allocPoint': allocPoint
# #                 }
# #                 result['totalAllocPoint']: totalAllocPoint
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_pool_info(web3, lptoken_address, block, blockchain, **kwargs):

#     result = {}

#     try:
#         use_db = kwargs['use_db']
#     except:
#         use_db = True

#     if use_db == True:
#         with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/sushi_swap.json', 'r') as db_file:
#             # Reading from json file
#             db_data = json.load(db_file)
        
#         if blockchain == ETHEREUM:
#             try:
#                 result['chef_contract'] = get_chef_contract(web3, block, blockchain)
#                 result['pool_info'] = {
#                     'poolId': db_data[blockchain]['poolsv2'][lptoken_address],
#                     'allocPoint': result['chef_contract'].functions.poolInfo(db_data[blockchain]['poolsv2'][lptoken_address]).call(block_identifier = block)[2]
#                 }
#                 result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier = block)

#                 return result
            
#             except:
#                 try:
#                     result['chef_contract'] = get_chef_contract(web3, block, blockchain, v1 = True)
#                     result['pool_info'] = {
#                         'poolId': db_data[blockchain]['poolsv1'][lptoken_address],
#                         'allocPoint': result['chef_contract'].functions.poolInfo(db_data[blockchain]['poolsv1'][lptoken_address]).call(block_identifier = block)[1]
#                     }
#                     result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier = block)

#                     return result
                
#                 except:
#                     return None
        
#         else:
#             try:
#                 result['chef_contract'] = get_chef_contract(web3, block, blockchain)
#                 result['pool_info'] = {
#                     'poolId': db_data[blockchain]['pools'][lptoken_address],
#                     'allocPoint': result['chef_contract'].functions.poolInfo(db_data[blockchain]['pools'][lptoken_address]).call(block_identifier = block)[2]
#                 }
#                 result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier = block)

#                 return result

#             except:
#                 return None
    
#     else:
#         result['chef_contract'] = get_chef_contract(web3, block, blockchain)

#         pool_length = result['chef_contract'].functions.poolLength().call(block_identifier = block)

#         for pool_id in range(pool_length):

#             address = result['chef_contract'].functions.lpToken(pool_id).call()

#             if address == lptoken_address:
#                 result['pool_info'] = {
#                     'poolId': pool_id,
#                     'allocPoint': result['chef_contract'].functions.poolInfo(pool_id).call(block_identifier = block)[2]
#                 }
#                 result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier = block)

#                 return result
        
#         # This section searches if the pool it's a V1 pool (only in ETHEREUM)
#         if blockchain == ETHEREUM:

#             result['chef_contract'] = get_chef_contract(web3, block, blockchain, v1 = True)

#             pool_length = result['chef_contract'].functions.poolLength().call(block_identifier = block)

#             for pool_id in range(pool_length):

#                 address = result['chef_contract'].functions.poolInfo(pool_id).call()[0]

#                 if address == lptoken_address:
#                     result['pool_info'] = {
#                         'poolId': pool_id,
#                         'allocPoint': result['chef_contract'].functions.poolInfo(pool_id).call(block_identifier = block)[1]
#                     }
#                     result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier = block)

#                     return result
        
#     # If the lptoken_address doesn't match with a V2 or V1 pool
#     return None

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_lptoken_data
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'web3' = web3 (Node) -> Improves performance
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_lptoken_data(lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts   
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         web3 = kwargs['web3']
#     except:
#         web3 = None

#     try:
#         if web3 == None: 
#             web3 = get_node(blockchain, block = block, index = index)

#         lptoken_data = {}
        
#         lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3 = web3, abi = ABI_LPTOKEN, block = block)
        
#         lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()
#         lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(block_identifier = block)
#         lptoken_data['token0'] = lptoken_data['contract'].functions.token0().call()
#         lptoken_data['token1'] = lptoken_data['contract'].functions.token1().call()
#         lptoken_data['reserves'] = lptoken_data['contract'].functions.getReserves().call(block_identifier = block)
#         lptoken_data['kLast'] = lptoken_data['contract'].functions.kLast().call(block_identifier = block)

#         root_k = math.sqrt(lptoken_data['reserves'][0] * lptoken_data['reserves'][1])
#         root_k_last = math.sqrt(lptoken_data['kLast'])
        
#         if root_k > root_k_last:
#             lptoken_data['virtualTotalSupply'] = lptoken_data['totalSupply'] * 6 * root_k / (5 * root_k + root_k_last)
#         else:
#             lptoken_data['virtualTotalSupply'] = lptoken_data['totalSupply']

#         return lptoken_data
    
#     except GetNodeLatestIndexError:
#         index = 0

#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution + 1)
    
#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution + 1)
    
#     except Exception as Ex:
#         traceback.print_exc()
#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_virtual_total_supply
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'web3' = web3 (Node) -> Improves performance
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_virtual_total_supply(lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0

#     try:
#         web3 = kwargs['web3']
#     except:
#         web3 = None

#     try:
#         if web3 == None:
#             web3 = get_node(blockchain, block = block, index = index)

#         lptoken_data = {}

#         lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3 = web3, abi = ABI_LPTOKEN, block = block)

#         lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(block_identifier = block)
#         lptoken_data['reserves'] = lptoken_data['contract'].functions.getReserves().call(block_identifier = block)
#         lptoken_data['kLast'] = lptoken_data['contract'].functions.kLast().call(block_identifier = block)

#         root_k = math.sqrt(lptoken_data['reserves'][0] * lptoken_data['reserves'][1])
#         root_k_last = math.sqrt(lptoken_data['kLast'])

#         return lptoken_data['totalSupply'] * 6 * root_k / (5 * root_k + root_k_last)

#     except GetNodeLatestIndexError:
#         index = 0

#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_rewarder_contract
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id):

#     rewarder_contract_address = chef_contract.functions.rewarder(pool_id).call()
#     rewarder_contract = get_contract(rewarder_contract_address, blockchain, web3 = web3, abi = ABI_REWARDER, block = block)
    
#     return rewarder_contract

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_sushi_rewards
# # **kwargs:
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output:
# # 1 - Tuple: [sushi_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_sushi_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, **kwargs):

#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     try:
#         sushi_address = chef_contract.functions.SUSHI().call()
#     except:
#         sushi_address = chef_contract.functions.sushi().call()

#     if decimals == True:
#         sushi_decimals = get_decimals(sushi_address, blockchain, web3 = web3)
#     else:
#         sushi_decimals = 0
    
#     sushi_rewards = chef_contract.functions.pendingSushi(pool_id, wallet).call(block_identifier = block) / (10**sushi_decimals)

#     return [sushi_address, sushi_rewards]

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_rewards
# # **kwargs:
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output:
# # 1 - List of Tuples: [reward_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, **kwargs):

#     rewards = []

#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True

#     rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)

#     pending_tokens_info = rewarder_contract.functions.pendingTokens(pool_id, wallet, 1).call(block_identifier = block)
#     pending_tokens_addresses = pending_tokens_info[0]
#     pending_token_amounts = pending_tokens_info[1]

#     for i in range(len(pending_tokens_addresses)):

#         if decimals == True:
#             reward_token_decimals = get_decimals(pending_tokens_addresses[i], blockchain, web3 = web3)
#         else:
#             reward_token_decimals = 0
        
#         reward_token_amount = pending_token_amounts[i] / (10**reward_token_decimals)

#         rewards.append([pending_tokens_addresses[i], reward_token_amount])

#     return rewards

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_all_rewards
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'web3' = web3 (Node) -> Improves performance
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # 'pool_info' = Dictionary -> Improves performance
# # Output:
# # 1 - List of Tuples: [reward_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_all_rewards(wallet, lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts   
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     try:
#         web3 = kwargs['web3']
#     except:
#         web3 = None
    
#     all_rewards = []

#     try:
#         if web3 == None: 
#             web3 = get_node(blockchain, block = block, index = index)

#         wallet = web3.toChecksumAddress(wallet)
        
#         lptoken_address = web3.toChecksumAddress(lptoken_address)
        
#         try:
#             pool_info = kwargs['pool_info']
#         except:
#             pool_info = get_pool_info(web3, lptoken_address, block, blockchain)
        
#         if pool_info == None:
#             print('Error: Incorrect Sushi LPToken Address: ', lptoken_address)
#             return None

#         pool_id = pool_info['pool_info']['poolId']
#         chef_contract = pool_info['chef_contract']

#         sushi_rewards = get_sushi_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals = decimals)
#         all_rewards.append(sushi_rewards)

#         if chef_contract.address != MASTERCHEF_V1:
#             rewards = get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals = decimals)

#             if len(rewards) > 0:
#                 for reward in rewards:
#                     all_rewards.append(reward)
        
#         return all_rewards

#     except GetNodeLatestIndexError:
#         index = 0

#         return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # underlying
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output: a list with 2 elements:
# # 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# # 2 - List of Tuples: [reward_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def underlying(wallet, lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         reward = kwargs['reward']
#     except:
#         reward = False
    
#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     result = []
#     balances = []

#     try:
#         web3 = get_node(blockchain, block = block, index = index)

#         wallet = web3.toChecksumAddress(wallet)
        
#         lptoken_address = web3.toChecksumAddress(lptoken_address)

#         pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

#         if pool_info == None:
#             print('Error: Incorrect Sushi LPToken Address: ', lptoken_address)
#             return None

#         pool_id = pool_info['pool_info']['poolId']
#         chef_contract = pool_info['chef_contract']

#         lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index)

#         pool_balance_fraction = lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier = block) / lptoken_data['virtualTotalSupply']
#         pool_staked_fraction =  chef_contract.functions.userInfo(pool_id, wallet).call(block_identifier = block)[0] / lptoken_data['virtualTotalSupply']

#         for i in range(len(lptoken_data['reserves'])):
#             try:
#                 getattr(lptoken_data['contract'].functions, 'token' + str(i))
#             except:
#                 continue
            
#             token_address = lptoken_data['token' + str(i)]

#             if decimals == True:
#                 token_decimals = get_decimals(token_address, blockchain, web3 = web3)
#             else:
#                 token_decimals = 0

#             token_balance = lptoken_data['reserves'][i] / (10**token_decimals) * (pool_balance_fraction)
#             token_staked = lptoken_data['reserves'][i] / (10**token_decimals) * (pool_staked_fraction)

#             balances.append([token_address, token_balance, token_staked])
        
#         if reward == True:
#             all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, pool_info = pool_info, index = index)
            
#             result.append(balances)
#             result.append(all_rewards)
       
#         else:
#             result = balances

#         return result
    
#     except GetNodeLatestIndexError:
#         index = 0

#         return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, index = index, execution = execution + 1)
    
#     except GetNodeArchivalIndexError:
#         index = 0
        
#         underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # pool_balances
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output: a list with 1 element:
# # 1 - List of Tuples: [liquidity_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def pool_balances(lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     balances = []

#     try:
#         web3 = get_node(blockchain, block = block, index = index)

#         lptoken_address = web3.toChecksumAddress(lptoken_address)
        
#         lptoken_contract = get_contract(lptoken_address, blockchain, web3 = web3, abi = ABI_LPTOKEN, block = block)

#         reserves = lptoken_contract.functions.getReserves().call(block_identifier = block)

#         for i in range(len(reserves)):
#             try:
#                 func = getattr(lptoken_contract.functions, 'token' + str(i))
#             except:
#                 continue

#             token_address = func().call()

#             if decimals == True:
#                 token_decimals = get_decimals(token_address, blockchain, web3 = web3)
#             else:
#                 token_balance = 0
            
#             token_balance = reserves[i] / (10**token_decimals)

#             balances.append([token_address, token_balance])

#         return balances

#     except GetNodeLatestIndexError:
#         index = 0

#         return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0

#         return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return pool_balances(lptoken_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # swap_fees
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def swap_fees(lptoken_address, block_start, block_end, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     result = {}
#     hash_overlap = []

#     try:
#         web3 = get_node(blockchain, block = block_start, index = index)

#         lptoken_address = web3.toChecksumAddress(lptoken_address)

#         lptoken_contract = get_contract(lptoken_address, blockchain, web3 = web3, abi = ABI_LPTOKEN)

#         token0 = lptoken_contract.functions.token0().call()
#         token1 = lptoken_contract.functions.token1().call()
#         result['swaps'] = []

#         if decimals == True:
#             decimals0 = get_decimals(token0, blockchain, web3 = web3)
#             decimals1 = get_decimals(token1, blockchain, web3 = web3)
#         else:
#             decimals0 = 0
#             decimals1 = 0

#         get_logs_bool = True
#         block_from = block_start
#         block_to = block_end

#         swap_event = web3.keccak(text = SWAP_EVENT_SIGNATURE).hex()

#         while get_logs_bool:
#             swap_logs = get_logs(block_from, block_to, lptoken_address, swap_event, blockchain)
            
#             log_count = len(swap_logs)

#             if log_count != 0:
#                 last_block = int(swap_logs[log_count - 1]['blockNumber'][2:len(swap_logs[log_count - 1]['blockNumber'])], 16)

#                 for swap_log in swap_logs:
#                     block_number = int(swap_log['blockNumber'][2:len(swap_log['blockNumber'])], 16)

#                     if swap_log['transactionHash'] in swap_log:
#                         continue

#                     if block_number == last_block:
#                         hash_overlap.append(swap_log['transactionHash'])

#                     if int(swap_log['data'][2:66], 16) == 0:
#                         swap_data = {
#                             'block': block_number,
#                             'token': token1,
#                             'amount': 0.003 * int(swap_log['data'][67:130], 16) / (10 ** decimals1)
#                         }
#                     else:
#                         swap_data = {
#                         'block': block_number,
#                         'token': token0,
#                         'amount': 0.003 * int(swap_log['data'][2:66], 16) / (10**decimals0)
#                         }

#                     result['swaps'].append(swap_data)
            
#             if log_count < 1000:
#                 get_logs_bool = False
            
#             else:
#                 block_from = block_number

#         return result
    
#     except GetNodeLatestIndexError:
#         index = 0

#         return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0

#         return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals = decimals, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_wallet_by_tx
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'signature' = signature of the type of transaction that will be searched for
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_wallet_by_tx(lptoken_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0

#     try:
#         signature = kwargs['signature']
#     except:
#         signature = DEPOSIT_EVENT_SIGNATURE

#     try:
#         web3 = get_node(blockchain, block = block, index = index)

#         lptoken_address = web3.toChecksumAddress(lptoken_address)
        
#         if isinstance(block, str):
#             if block == 'latest':
#                 block = last_block(blockchain, web3 = web3)
        
#         chef_contract = get_pool_info(web3, lptoken_address, block, blockchain)[0]

#         if chef_contract != None:
        
#             tx_hex_bytes = Web3.keccak(text = signature)[0:4].hex()

#             block_start = block
#             while True:

#                 block_start = block_start - 1000000
                
#                 lptoken_txs = get_token_tx(lptoken_address, chef_contract.address, block_start, block, blockchain)

#                 for lptoken_tx in lptoken_txs:
#                     txs = get_tx_list(lptoken_tx['from'], block_start, block, blockchain)
                
#                     for tx in txs:
                        
#                         if tx['input'][0:10] == tx_hex_bytes:
#                             return tx['from']
       
#     except GetNodeLatestIndexError:
#         index = 0

#         return get_wallet_by_tx(lptoken_address, block, blockchain, signature = signature, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_wallet_by_tx(lptoken_address, block, blockchain, signature = signature, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_wallet_by_tx(lptoken_address, block, blockchain, signature = signature, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_rewards_per_unit
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'block' = block identifier
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_rewards_per_unit(lptoken_address, blockchain, **kwargs):

#     result = []

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         block = kwargs['block']
#     except:
#         block = 'latest'

#     try:
#         web3 = get_node(blockchain, block = block, index = index)

#         lptoken_address = web3.toChecksumAddress(lptoken_address)
        
#         pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

#         if pool_info == None:
#             print('Error: Incorrect Sushi LPToken Address: ', lptoken_address)
#             return None

#         chef_contract = pool_info['chef_contract']
#         pool_id = pool_info['pool_info']['poolId']

#         sushi_reward_data = {}

#         try:
#             sushi_reward_data['sushi_address'] = chef_contract.functions.SUSHI().call()
#         except:
#             sushi_reward_data['sushi_address'] = chef_contract.functions.sushi().call()
        
#         try:
#             sushi_reward_data['sushiPerBlock'] = chef_contract.functions.sushiPerBlock().call(block_identifier = block) * (pool_info['pool_info']['allocPoint'] / pool_info['totalAllocPoint'])
#         except:
#             sushi_reward_data['sushiPerSecond'] = chef_contract.functions.sushiPerSecond().call(block_identifier = block) * (pool_info['pool_info']['allocPoint'] / pool_info['totalAllocPoint'])
        
#         result.append(sushi_reward_data)

#         try:
#             reward_data = {}

#             rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)
#             rewarder_pool_info = rewarder_contract.functions.poolInfo(pool_id).call(block_identifier = block)
#             rewarder_alloc_point = rewarder_pool_info[2]

#             # Rewarder Total Allocation Point Calculation
#             rewarder_total_alloc_point = 0
#             for i in range(chef_contract.functions.poolLength().call()):
#                 rewarder_total_alloc_point += rewarder_contract.functions.poolInfo(i).call(block_identifier = block)[2]

#             reward_data['reward_address'] = rewarder_contract.functions.pendingTokens(pool_id, ZERO_ADDRESS, 1).call(block_identifier = block)[0][0]
            
#             try:
#                 reward_data['rewardPerSecond'] = rewarder_contract.functions.rewardPerSecond().call(block_identifier = block) * (rewarder_alloc_point / rewarder_total_alloc_point)
#             except:
#                 reward_data['rewardPerSecond'] = 0

#             result.append(reward_data)
        
#         except:
#             pass

#         return result

#     except GetNodeLatestIndexError:
#         index = 0

#         return get_rewards_per_unit(lptoken_address, blockchain, block = block, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_rewards_per_unit(lptoken_address, blockchain, block = block, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_rewards_per_unit(lptoken_address, blockchain, block = block, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_apr
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'block' = block identifier
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_apr(lptoken_address, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         block = kwargs['block']
#     except:
#         block = 'latest'

#     try:
#         data = get_rewards_per_unit(lptoken_address, blockchain, block = block)

#         sushi_price = Prices.get_price(data[0]['sushi_address'], block, blockchain)
#         sushi_decimals = get_decimals(data[0]['sushi_address'], blockchain)

#         try:
#             sushi_per_block = data[0]['sushiPerBlock']
#             blocks_per_year = get_blocks_per_year(blockchain)
#             sushi_per_year = sushi_per_block * blocks_per_year / (10**sushi_decimals)
#         except:
#             sushi_per_second = data[0]['sushiPerSecond']
#             sushi_per_year = sushi_per_second * (3600 * 24 * 365) / (10**sushi_decimals)
        
#         try:
#             reward_price = Prices.get_price(data[1]['reward_address'], block, blockchain)
#             reward_decimals = get_decimals(data[1]['reward_address'], blockchain)

#             reward_per_year = data[1]['rewardPerSecond'] * (3600 * 24 * 365) / (10**reward_decimals)
#         except:
#             reward_price = 0
#             reward_per_year = 0

#         balances = pool_balances(lptoken_address, block, blockchain)
#         token_addresses = [balances[i][0] for i in range(len(balances))]
#         token_prices = [Prices.get_price(token_addresses[i], block, blockchain) for i in range(len(token_addresses))]
#         tvl = sum([balances[i][1] * token_prices[i] for i in range(len(token_addresses))])

#         apr = ((sushi_per_year * sushi_price + reward_per_year * reward_price) / tvl) * 100

#         return apr

#     except GetNodeLatestIndexError:
#         index = 0

#         return get_apr(lptoken_address, blockchain, block = block, index = index, execution = execution + 1)

#     except GetNodeArchivalIndexError:
#         index = 0
        
#         return get_apr(lptoken_address, blockchain, block = block, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_apr(lptoken_address, blockchain, block = block, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # update_db
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def update_db():

#     update = False

#     with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/sushi_swap.json', 'r') as db_file:
#         # Reading from json file
#         db_data = json.load(db_file)
    
#     web3 = get_node(ETHEREUM)

#     master_chefv2 = get_chef_contract(web3, 'latest', ETHEREUM)
#     db_pool_length = len(db_data[ETHEREUM]['poolsv2'])
#     pools_delta = master_chefv2.functions.poolLength().call() - db_pool_length
    
#     if pools_delta > 0:

#         update = True
        
#         for i in range(pools_delta):
#             lptoken_address = master_chefv2.functions.lpToken(db_pool_length + i).call()
#             db_data[ETHEREUM]['poolsv2'][lptoken_address] = db_pool_length + i
    
#     master_chefv1 = get_chef_contract(web3, 'latest', ETHEREUM, v1 = True)
#     db_pool_length = len(db_data[ETHEREUM]['poolsv1'])
#     pools_delta = master_chefv1.functions.poolLength().call() - db_pool_length
    
#     if pools_delta > 0:

#         update = True
        
#         for i in range(pools_delta):
#             lptoken_address = master_chefv1.functions.poolInfo(db_pool_length + i).call()[0]
#             db_data[ETHEREUM]['poolsv1'][lptoken_address] = db_pool_length + i

#     web3 = get_node(POLYGON)

#     mini_chef = get_chef_contract(web3, 'latest', POLYGON)
#     db_pool_length = len(db_data[POLYGON]['pools'])
#     pools_delta = mini_chef.functions.poolLength().call() - db_pool_length
    
#     if pools_delta > 0:

#         update = True
        
#         for i in range(pools_delta):
#             lptoken_address = mini_chef.functions.lpToken(db_pool_length + i).call()
#             db_data[POLYGON]['pools'][lptoken_address] = db_pool_length + i
    
#     web3 = get_node(XDAI)
    
#     mini_chef = get_chef_contract(web3, 'latest', XDAI)
#     db_pool_length = len(db_data[XDAI]['pools'])
#     pools_delta = mini_chef.functions.poolLength().call() - db_pool_length
    
#     if pools_delta > 0:

#         update = True
        
#         for i in range(pools_delta):
#             lptoken_address = mini_chef.functions.lpToken(db_pool_length + i).call()
#             db_data[XDAI]['pools'][lptoken_address] = db_pool_length + i

#     if update == True:
#         with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/db/sushi_swap.json', 'w') as db_file:
#             json.dump(db_data, db_file)
