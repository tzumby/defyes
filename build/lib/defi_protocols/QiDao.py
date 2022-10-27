# from general.blockchain_functions import *
# from price_feeds import Prices

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # QIDAO_VAULTS
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # QiDao Vaults List
# QIDAO_VAULTS = [
#     {
#         'blockchain': XDAI,
#         'vaults': [
#             {
#                 'collateral': GNO_XDAI,
#                 'address': '0x014A177E9642d1b4E970418f894985dC1b85657f' # GNO Vault Address
#             },
#             {
#                 'collateral': WETH_XDAI,
#                 'address': '0x5c49b268c9841AFF1Cc3B0a418ff5c3442eE3F3b' # WETH Vault Address
#             }
#         ]
#     },

#     {
#         'blockchain': POLYGON,
#         'vaults': []
#     }
# ]

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # ABIs
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # Vault ABI - _minimumCollateralPercentage, checkCollateralPercentage, exists, getDebtCeiling, getEthPriceSource, getTokenPriceSource, mai, priceSourceDecimals, vaultCollateral, vaultDebt 
# ABI_VAULT = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"_minimumCollateralPercentage","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"checkCollateralPercentage","inputs":[{"type":"uint256","name":"vaultID","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"exists","inputs":[{"type":"uint256","name":"vaultID","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getDebtCeiling","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getEthPriceSource","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getTokenPriceSource","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"contract ERC20Detailed"}],"name":"mai","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"priceSourceDecimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"vaultCollateral","inputs":[{"type":"uint256","name":"","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"vaultDebt","inputs":[{"type":"uint256","name":"","internalType":"uint256"}],"constant":true}]'


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_vault_address
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_vault_address(collateral_address, blockchain):

#     vault_address = None

#     for qidao_vault in QIDAO_VAULTS:

#         if qidao_vault['blockchain'] == blockchain:

#             for vault in qidao_vault['vaults']:

#                 if vault['collateral'] == collateral_address:

#                     vault_address = vault['address']
#                     break
            
#             break
    
#     return vault_address

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_vault_data
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'web3' = web3 (Node) -> Improves performance
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_vault_data(vault_id, collateral_address, block, blockchain, **kwargs):

#     try:
#         execution = kwargs['execution']
#     except:
#         execution = 1

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts   
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         web3 = kwargs['web3']
#     except:
#         web3 = None

#     try:
#         index = kwargs['index']
#     except:
#         index = 0
    
#     try:
#         decimals = kwargs['decimals']
#     except:
#         decimals = True
    
#     vault_data = {}
    
#     try:
#         if web3 == None: 
#             web3 = get_node(blockchain, block = block, index = index)

#         collateral_address = web3.toChecksumAddress(collateral_address)
        
#         vault_address = get_vault_address(collateral_address, blockchain)

#         if vault_address != None:
#             vault_contract = get_contract(vault_address, blockchain, web3 = web3, block = block)

#             if vault_contract.functions.exists(vault_id).call(block_identifier = block):

#                 debt_address = vault_contract.functions.mai().call()

#                 debt_decimals = get_decimals(debt_address, blockchain, web3 = web3)
#                 collateral_decimals = get_decimals(collateral_address, blockchain, web3 = web3)
                
#                 vault_collateral = vault_contract.functions.vaultCollateral(vault_id).call(block_identifier = block)
#                 vault_debt = vault_contract.functions.vaultDebt(vault_id).call(block_identifier = block)

#                 price_source_decimals = vault_contract.functions.priceSourceDecimals().call()

#                 # Collateral Address
#                 vault_data['collateral_address'] = collateral_address

#                 # Collateral Amount
#                 if decimals == True:
#                     vault_data['collateral_amount'] = vault_collateral / (10**collateral_decimals)
#                 else:
#                     vault_data['collateral_amount'] = vault_collateral

#                 # Collateral Token USD Value
#                 vault_data['collateral_token_usd_value'] = vault_contract.functions.getEthPriceSource().call(block_identifier = block) / (10**price_source_decimals)

#                 # Debt Address
#                 vault_data['debt_address'] = debt_address
     
#                 # Debt Amount
#                 if decimals == True:
#                     vault_data['debt_amount'] = vault_debt / (10**debt_decimals)
#                 else:
#                     vault_data['debt_amount'] = vault_debt
        
#                 # Debt Token USD Value
#                 # getTokenPriceSource() always returns MAI price = 1 USD. This is the price QiDao uses to calculate the Collateral Ratio.
#                 # MAI price might have depegged from USD so afterwards vault_data['debt_token_usd_value'] is overwritten with the price obtained from CoinGecko
#                 vault_data['debt_token_usd_value'] = vault_contract.functions.getTokenPriceSource().call(block_identifier = block) / (10**price_source_decimals)
        
#                 # Debt USD Value
#                 vault_data['debt_usd_value'] = (vault_debt / (10**debt_decimals)) * vault_data['debt_token_usd_value']

#                  # Collateral Ratio
#                 vault_data['collateral_ratio'] = (((vault_collateral / (10**collateral_decimals)) * vault_data['collateral_token_usd_value']) / vault_data['debt_usd_value']) * 100

#                 # Available Debt Amount to Borrow
#                 if decimals == True:
#                     vault_data['available_debt_amount'] = vault_contract.functions.getDebtCeiling().call(block_identifier = block) / (10**debt_decimals)
#                 else:
#                     vault_data['available_debt_amount'] = vault_contract.functions.getDebtCeiling().call(block_identifier = block)

#                 # Liquidation Ratio
#                 vault_data['liquidation_ratio'] = vault_contract.functions._minimumCollateralPercentage().call(block_identifier = block)

#                 # Liquidation Price
#                 vault_data['liquidation_price'] = ((vault_data['liquidation_ratio'] / 100) * vault_data['debt_usd_value']) / (vault_collateral / (10**collateral_decimals))

#                 # Debt Token USD Value OVERWRITTEN WITH COINGECKO'S PRICE
#                 vault_data['debt_token_usd_value'] = Prices.get_price(MAI_POL, 'latest', POLYGON)
#                 # price_data = getPriceCoinGecko(MAI_POL, math.floor(datetime.now().timestamp()), POLYGON)
                
#                 # while price_data[0] == 429:
#                 #     time.sleep(COINGECKO_COOLDOWN)
#                 #     price_data = getPriceCoinGecko(MAI_POL, math.floor(datetime.now().timestamp()), POLYGON)
                
#                 # vault_data['debt_token_usd_value'] = price_data[1][1]

#         return vault_data

#     except GetNodeLatestIndexError:
#         index = 0

#         return get_vault_data(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
#     except GetNodeArchivalIndexError:
#         index = 0

#         return get_vault_data(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
#     except Exception as Ex:
#         traceback.print_exc()
#         return get_vault_data(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # underlying
# # **kwargs:
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# # Output:
# # 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def underlying(vault_id, collateral_address, block, blockchain, **kwargs):

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
    
#     result = []

#     try:
#         web3 = get_node(blockchain, block = block, index = index)
        
#         collateral_address = web3.toChecksumAddress(collateral_address)
        
#         vault_address = get_vault_address(collateral_address, blockchain)

#         if vault_address != None:
#             vault_contract = get_contract(vault_address, blockchain, web3 = web3, block = block)

#             if vault_contract.functions.exists(vault_id).call(block_identifier = block):
                
#                 if decimals == True:
#                     collateral_decimals = get_decimals(collateral_address, blockchain, web3 = web3)
#                 else:
#                     collateral_decimals = 0

#                 collateral_amount = vault_contract.functions.vaultCollateral(vault_id).call(block_identifier = block) / (10**collateral_decimals)
                
#                 result.append([collateral_address, collateral_amount])

#                 debt_address = vault_contract.functions.mai().call()

#                 if decimals == True:
#                     debt_decimals = get_decimals(debt_address, blockchain, web3 = web3)
#                 else:
#                     debt_decimals = 0

#                 debt_amount = -1 * vault_contract.functions.vaultDebt(vault_id).call(block_identifier = block) / (10**debt_decimals)

#                 result.append([debt_address, debt_amount])

#         return result

#     except GetNodeLatestIndexError:
#         index = 0

#         return underlying(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)
    
#     except GetNodeArchivalIndexError:
#         index = 0
        
#         return underlying(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index, execution = execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return underlying(vault_id, collateral_address, block, blockchain, decimals = decimals, index = index + 1, execution = execution)
