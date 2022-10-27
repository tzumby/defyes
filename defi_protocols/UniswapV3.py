from general.blockchain_functions import *

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNISWAP V3 FACTORY
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Factory Address
FACTORY = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FEES
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Possible Fees for Uniwsap v3 Pools
FEES = [100, 500, 3000, 10000]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Factory ABI - getPool
ABI_FACTORY = '[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Uniswap v3 Pools ABI - slot0, token0, token1
ABI_POOL = '[{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rate_uniswap_v3
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rate_uniswap_v3(token_src, token_dst, block, blockchain, **kwargs):

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
        fee = kwargs['fee']
    except:
        fee = 100
    
    try:
        web3 = get_node(blockchain, block = block, index = index)

        token_src = web3.toChecksumAddress(token_src)
        
        token_dst = web3.toChecksumAddress(token_dst)
        
        factory_contract = get_contract(FACTORY, blockchain, web3 = web3, abi = ABI_FACTORY, block = block)

        pool_address = factory_contract.functions.getPool(token_src, token_dst, fee).call()

        pool_contract = get_contract(pool_address, blockchain, web3 = web3, abi = ABI_POOL, block = block)

        sqrt_price_x96 = pool_contract.functions.slot0().call(block_identifier = block)[0]
        token0 = pool_contract.functions.token0().call()
        token1 = pool_contract.functions.token1().call()

        token_src_decimals = get_decimals(token_src, blockchain, web3 = web3)
        token_dst_decimals = get_decimals(token_dst, blockchain, web3 = web3)

        if token_src == token0:
            rate = (sqrt_price_x96 ** 2 / 2 ** 192) / (10 ** (token_dst_decimals - token_src_decimals))
        elif token_src == token1:
            rate = (2 ** 192 / sqrt_price_x96 ** 2) / (10 ** (token_dst_decimals - token_src_decimals))

        return rate
    
    except GetNodeLatestIndexError:
        index = 0

        return get_rate_uniswap_v3(token_src, token_dst, block, blockchain, index = index, execution = execution + 1)
    
    except GetNodeArchivalIndexError:
        index = 0
        
        return get_rate_uniswap_v3(token_src, token_dst, block, blockchain, index = index, execution = execution + 1)

    except Exception as Ex:
        traceback.print_exc()
        return get_rate_uniswap_v3(token_src, token_dst, block, blockchain, index = index + 1, execution = execution)

# weth_price = getPriceCoinGecko('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', math.floor(datetime.now().timestamp()), ETHEREUM)[1][1]
# rate = getRateUniswapV3('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'latest', ETHEREUM)
# usdc_price = weth_price * rate
# print(usdc_price)

# usdc_price = getPriceCoinGecko('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', math.floor(datetime.now().timestamp()), ETHEREUM)[1][1]
# rate = getRateUniswapV3('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', 'latest', ETHEREUM)
# weth_price = usdc_price * rate
# print(weth_price)

