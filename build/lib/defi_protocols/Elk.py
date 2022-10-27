# from general.blockchain_functions import *
# from price_feeds import Prices

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # LITERALS
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # API Call - List of the latest pools
# API_ELK_POOLS = 'https://api.elk.finance/v2/info/latest_pools'

# # Wrapped
# WRAPPED = 'wrapped'

# # Matic
# MATIC = 'matic'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # ABIs
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast
# ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"kLast","inputs":[],"constant":true}]'

# # Pool ABI - balanceOf, boosterEarned, boosterToken, earned, rewardsToken, totalSupply, boosterRewardPerToken, rewardPerToken
# ABI_POOL = '[{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"boosterEarned","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"boosterToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"earned","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"rewardsToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"boosterRewardPerToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"rewardPerToken","inputs":[]}]'

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # EVENT SIGNATURES
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Swap Event Signature
# SWAP_EVENT_SIGNATURE = 'Swap(address,uint256,uint256,uint256,uint256,address)'


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
        
#         # WARNING: Fees are deactivated in Elk
#         lptoken_data['virtualTotalSupply'] = lptoken_data['totalSupply']

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
# # get_pool_address
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_pool_address(web3, token0, token1, block, blockchain):

#     token0_contract = get_contract(token0, blockchain, web3 = web3, abi = ABI_TOKEN_SIMPLIFIED, block = block)
#     token1_contract = get_contract(token1, blockchain, web3 = web3, abi = ABI_TOKEN_SIMPLIFIED, block = block)

#     symbol0 = token0_contract.functions.symbol().call()
#     symbol1 = token1_contract.functions.symbol().call()

#     if WRAPPED in token0_contract.functions.name().call().lower():
#         symbol0 = symbol0[1:len(symbol0)]
    
#     if WRAPPED in token1_contract.functions.name().call().lower():
#         symbol1 = symbol1[1:len(symbol1)]
    
#     if blockchain == POLYGON:
#         blockchain = MATIC
    
#     # Special Case: symbol = 'XGT' -> XGTV2
#     if symbol0 == 'XGT':
#         symbol0 += 'V2'
    
#     if symbol1 == 'XGT':
#         symbol1 += 'V2'
    
#     # # Special Case: symbol = 'XCOMB' -> 'xCOMB
#     # if symbol0 == 'XCOMB':
#     #     symbol0 += 'xCOMB'
    
#     # if symbol1 == 'XCOMB':
#     #     symbol1 += 'xCOMB'

#     pools = requests.get(API_ELK_POOLS).json()

#     try:
#         pool_id = symbol0 + '-' + symbol1
#         pool_address = pools[blockchain][pool_id]['address']
    
#     except:
#         try:
#             pool_id = symbol1 + '-' + symbol0
#             pool_address = pools[blockchain][pool_id]['address']
        
#         except:
#             pool_address = None

#     return pool_address

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_elk_rewards
# # **kwargs:
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output:
# # 1 - Tuple: [elk_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_elk_rewards(web3, pool_contract, wallet, block, blockchain, **kwargs):

#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True

#     elk_token_address = pool_contract.functions.rewardsToken().call()

#     if decimals == True:
#         elk_token_decimals = get_decimals(elk_token_address, blockchain, web3 = web3)
#     else:
#         elk_token_decimals = 0
    
#     elk_rewards = pool_contract.functions.earned(wallet).call(block_identifier = block) / (10**elk_token_decimals)
    
#     return [elk_token_address, elk_rewards]

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_booster_rewards
# # **kwargs:
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output:
# # 1 - List of Tuples: [reward_token_address, balance]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_booster_rewards(web3, pool_contract, wallet, block, blockchain, **kwargs):

#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True

#     booster_token_address = pool_contract.functions.boosterToken().call()

#     if booster_token_address != ZERO_ADDRESS:
#         if decimals == True:
#             booster_token_decimals = get_decimals(booster_token_address, blockchain, web3 = web3)
#         else:
#             booster_token_decimals = 0
        
#         booster_rewards = pool_contract.functions.boosterEarned(wallet).call(block_identifier = block) / (10**booster_token_decimals)
    
#     else:
#         return None

#     return [booster_token_address, booster_rewards]

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_all_rewards
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'web3' = web3 (Node) -> Improves performance
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'pool_contract' -> Improves performance
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
#             pool_contract = kwargs['pool_contract']
#         except:
#             lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3 = web3)

#             pool_address = get_pool_address(web3, lptoken_data['token0'], lptoken_data['token1'], block, blockchain)
#             pool_contract = get_contract(pool_address, blockchain, web3 = web3, abi = ABI_POOL, block = block)

#         elk_rewards = get_elk_rewards(web3, pool_contract, wallet, block, blockchain, decimals = decimals)
#         all_rewards.append(elk_rewards)
        
#         booster_rewards = get_booster_rewards(web3, pool_contract, wallet, block, blockchain, decimals = decimals)
#         if booster_rewards != None:
#             all_rewards.append(booster_rewards)
        
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
        
#         lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution)

#         pool_address = get_pool_address(web3, lptoken_data['token0'], lptoken_data['token1'], block, blockchain)

#         if pool_address == None:
#             print('Error: Cannot find Elk Pool Address for LPToken Address: ', lptoken_address)
#             return None

#         pool_contract = get_contract(pool_address, blockchain, web3 = web3, abi = ABI_POOL, block = block)

#         # WARNING: Fees are deactivated in Elk
#         pool_balance_fraction = lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier = block) / lptoken_data['totalSupply']
#         pool_staked_fraction =  pool_contract.functions.balanceOf(wallet).call(block_identifier = block) / lptoken_data['totalSupply']

#         for i in range(len(lptoken_data['reserves']) - 1):
            
#             if i == 0:
#                 token_address = lptoken_data['token0']
            
#             elif i == 1:
#                 token_address = lptoken_data['token1']
            
#             if decimals == True:
#                 token_decimals = get_decimals(token_address, blockchain, web3 = web3)
#             else:
#                 token_decimals = 0

#             token_balance = lptoken_data['reserves'][i] / (10**token_decimals) * (pool_balance_fraction)
#             token_staked = lptoken_data['reserves'][i] / (10**token_decimals) * (pool_staked_fraction)

#             balances.append([token_address, token_balance, token_staked])
        
#         if reward == True:
#             all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3 = web3, decimals = decimals, pool_contract = pool_contract, index = index)
            
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
        
#         return underlying(wallet, lptoken_address, block, blockchain, reward = reward, decimals = decimals, index = index, execution = execution + 1)

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

#         for i in range(len(reserves) - 1):
#             try:
#                 func = getattr(lptoken_contract.functions, 'token' + str(i))
#             except:
#                 continue

#             token_address = func().call()
            
#             if decimals == True:
#                 token_decimals = get_decimals(token_address, blockchain, web3 = web3)
#                 token_balance = reserves[i] / (10 ** token_decimals)
#             else:
#                 token_balance = reserves[i]

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
#                             'block': block_number,
#                             'token': token0,
#                             'amount': 0.003 * int(swap_log['data'][2:66], 16) / (10 ** decimals0)
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
#         web3 = get_node(blockchain, block = block, index = index)
        
#         lptoken_address = web3.toChecksumAddress(lptoken_address)
#         lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3 = web3, index = index, execution = execution)

#         pool_address = get_pool_address(web3, lptoken_data['token0'], lptoken_data['token1'], block, blockchain)

#         if pool_address == None:
#             print('Error: Cannot find Elk Pool Address for LPToken Address: ', lptoken_address)
#             return None

#         pool_contract = get_contract(pool_address, blockchain, web3 = web3, abi = ABI_POOL, block = block)

#         booster_token = pool_contract.functions.boosterToken().call()
#         if booster_token != None and booster_token != ZERO_ADDRESS:
#             booster_token_decimals = get_decimals(booster_token, blockchain, web3 = web3)
#             booster_reward_per_token = pool_contract.functions.boosterRewardPerToken().call(block_identifier = block) / (10**booster_token_decimals)
#             booster_token_price = Prices.get_price(booster_token, block, blockchain)
#         else:
#             booster_reward_per_token = 0
#             booster_token_price = 0

#         rewards_token = pool_contract.functions.rewardsToken().call()
#         rewards_token_decimals = get_decimals(rewards_token, blockchain, web3 = web3)
#         reward_per_token = pool_contract.functions.rewardPerToken().call(block_identifier = block) / (10**rewards_token_decimals)
#         rewards_token_price = Prices.get_price(rewards_token, block, blockchain)

#         total_rewards = (booster_reward_per_token * booster_token_price + reward_per_token * rewards_token_price) * (lptoken_data['totalSupply'] / (10**lptoken_data['decimals']))

#         balances = pool_balances(lptoken_address, block, blockchain)
#         token_addresses = [balances[i][0] for i in range(len(balances))]
#         token_prices = [Prices.get_price(token_addresses[i], block, blockchain) for i in range(len(token_addresses))]
#         tvl = sum([balances[i][1] * token_prices[i] for i in range(len(token_addresses))])

#         apr = ((total_rewards) / tvl) * 100

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
