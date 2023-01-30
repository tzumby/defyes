from defi_protocols.functions import *
# import os
# from dotenv import load_dotenv
# load_dotenv()
from decimal import *

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNISWAP V3 FACTORY
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Factory Address
FACTORY = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNISWAP V3 POSITIONS NFT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Positions NFT
POSITIONS_NFT = '0xC36442b4a4522E871399CD717aBDD847Ab11FE88'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNISWAP V3 ROUTER 2
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Router 2
UNISWAPV3_ROUTER2 = '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FEES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Possible Fees for Uniwsap v3 Pools
FEES = [100, 500, 3000, 10000]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uniswap v3 Factory ABI - getPool
ABI_FACTORY = '[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Uniswap v3 Pools ABI - slot0, token0, token1
ABI_POOL = '[{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"}, \
            {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, \
            {"inputs":[],"name":"feeGrowthGlobal0X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"feeGrowthGlobal1X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, \
            {"inputs":[{"internalType":"int24","name":"","type":"int24"}],"name":"ticks","outputs":[{"internalType":"uint128","name":"liquidityGross","type":"uint128"},{"internalType":"int128","name":"liquidityNet","type":"int128"},{"internalType":"uint256","name":"feeGrowthOutside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthOutside1X128","type":"uint256"},{"internalType":"int56","name":"tickCumulativeOutside","type":"int56"},{"internalType":"uint160","name":"secondsPerLiquidityOutsideX128","type":"uint160"},{"internalType":"uint32","name":"secondsOutside","type":"uint32"},{"internalType":"bool","name":"initialized","type":"bool"}],"stateMutability":"view","type":"function"}]'

# Uniswap v3 NFT manager - balanceOf, tokenofownerbyindex, positions, ownerof
ABI_POSITIONS_NFT = '[{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"positions","outputs":[{"internalType":"uint96","name":"nonce","type":"uint96"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0","type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BASETICK
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Basetick calculations
BASETICK = 1.0001


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rate_uniswap_v3
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'fee' = fee
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rate_uniswap_v3(token_src, token_dst, block, blockchain, web3=None, execution=1, index=0, fee=100):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        token_src = web3.toChecksumAddress(token_src)

        token_dst = web3.toChecksumAddress(token_dst)

        factory_contract = get_contract(FACTORY, blockchain, web3=web3, abi=ABI_FACTORY, block=block)

        pool_address = factory_contract.functions.getPool(token_src, token_dst, fee).call(block_identifier=block)

        pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)

        sqrt_price_x96 = pool_contract.functions.slot0().call(block_identifier=block)[0]
        token0 = pool_contract.functions.token0().call(block_identifier=block)
        token1 = pool_contract.functions.token1().call(block_identifier=block)

        token_src_decimals = get_decimals(token_src, blockchain, web3=web3)
        token_dst_decimals = get_decimals(token_dst, blockchain, web3=web3)

        if token_src == token0:
            rate = float(Decimal(sqrt_price_x96 ** 2) / Decimal(2 ** 192) / Decimal(10 ** (token_dst_decimals - token_src_decimals)))
        elif token_src == token1:
            rate = float(Decimal(2 ** 192) / Decimal(sqrt_price_x96 ** 2) / Decimal(10 ** (token_dst_decimals - token_src_decimals)))


        return rate

    except GetNodeIndexError:
        return get_rate_uniswap_v3(token_src, token_dst, block, blockchain, fee=fee, index=0, execution=execution + 1)

    except:
        return get_rate_uniswap_v3(token_src, token_dst, block, blockchain, fee=fee, index=index + 1,
                                   execution=execution)


def underlying(wallet, nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.toChecksumAddress(wallet)
        factory_address = get_contract(FACTORY, blockchain, web3=web3, abi=ABI_FACTORY, block=block)
        nft_contract = get_contract(POSITIONS_NFT, blockchain, web3=web3, abi=ABI_POSITIONS_NFT, block=block)
        nft_owner = nft_contract.functions.ownerOf(nftid).call(block_identifier=block)
        if nft_owner == wallet:
            nft_positions = nft_contract.functions.positions(nftid).call(block_identifier=block)
            upper_tick = int(nft_positions[6])
            lower_tick = int(nft_positions[5])
            token0 = nft_positions[2]
            token1 = nft_positions[3]
            fee = nft_positions[4]
            liquidity = Decimal(nft_positions[7])


            if liquidity != 0:
                if decimals is True:
                    decimals0 = get_decimals(token0, blockchain, web3=web3)
                    decimals1 = get_decimals(token1, blockchain, web3=web3)

                pool_address = factory_address.functions.getPool(token0, token1, fee).call(block_identifier=block)
                pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)
                current_tick = pool_contract.functions.slot0().call(block_identifier=block)[1]
                sqrt_price_X96 = pool_contract.functions.slot0().call(block_identifier=block)[0]

                sa = Decimal(BASETICK) ** Decimal(lower_tick / 2)
                sb = Decimal(BASETICK) ** Decimal(upper_tick / 2)
                current_square_price = Decimal(sqrt_price_X96) / Decimal(2**96)

                if upper_tick <= current_tick:
                    amount1 = (liquidity * (sb - sa))
                    if decimals is True:
                        amount1 = float(amount1 / Decimal(10 ** decimals1))
                    else:
                        amount1 = int(amount1)
                    balances.append([token1, amount1])
                elif lower_tick < current_tick < upper_tick:
                    amount0 = (liquidity * (sb - current_square_price) / (current_square_price * sb))
                    amount1 = (liquidity * (current_square_price - sa))

                    if decimals is True:
                        amount0 = float(amount0 / Decimal(10 ** decimals0))
                        amount1 = float(amount1 / Decimal(10 ** decimals1))
                    else:
                        amount0 = int(amount0)
                        amount1 = int(amount1)

                    balances.append([token0, amount0])
                    balances.append([token1, amount1])

                else:
                    amount0 = (liquidity * (sb - sa) / (sa * sb))
                    if decimals is True:
                        amount0 = float(amount0 / Decimal(10 ** decimals0))
                    else:
                        amount0 = int(amount0)
                    balances.append([token0, amount0])
            else:
                balances.append([token0, 0])
                balances.append([token1, 0])
            return balances
        else:
            return 'wallet is not owner of this NFT'

    except GetNodeIndexError:
        return underlying(wallet, nftid, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, nftid, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


def allnfts(wallet, block, blockchain, web3=None, execution=1, index=0):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    nftids = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        nft_contract = get_contract(POSITIONS_NFT, blockchain, web3=web3, abi=ABI_POSITIONS_NFT, block=block)
        nft_balance = nft_contract.functions.balanceOf(wallet).call(block_identifier=block)
        for i in range(0, nft_balance):
            nft_id = nft_contract.functions.tokenOfOwnerByIndex(wallet, i).call(block_identifier=block)
            nftids.append(nft_id)
        return nftids

    except GetNodeIndexError:
        return allnfts(wallet, block, blockchain, index=0, execution=execution + 1)

    except:
        return allnfts(wallet, block, blockchain, index=index + 1, execution=execution)


def underlying_all(wallet, block, blockchain):
    balances = []
    for nft in allnfts(wallet, block, blockchain):
        balances.append(underlying(wallet, nft, block, blockchain))
    return list(filter(None, balances))


##to test
# wallet='0x849D52316331967b6fF1198e5E32A0eB168D039d'
# id = 286920
# uniswapv3 = underlying(wallet,id,'latest',ETHEREUM)
# print(uniswapv3)
# nfts_list = allnfts(wallet, 'latest', ETHEREUM)
# print(nfts_list)
# nfts = underlying_all(wallet,'latest',ETHEREUM)
# print(nfts)

def get_fee(nftid, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    if execution > MAX_EXECUTIONS:
        return None

    fees = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        factory_address = get_contract(FACTORY, blockchain, web3=web3, abi=ABI_FACTORY, block=block)
        nft_contract = get_contract(POSITIONS_NFT, blockchain, web3=web3, abi=ABI_POSITIONS_NFT, block=block)
        nft_positions = nft_contract.functions.positions(nftid).call(block_identifier=block)
        upper_tick = nft_positions[6]
        lower_tick = nft_positions[5]
        token0 = nft_positions[2]
        token1 = nft_positions[3]
        fee = nft_positions[4]
        liquidity = nft_positions[7]
        pool_address = factory_address.functions.getPool(token0, token1, fee).call(block_identifier=block)
        pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)
        current_tick = pool_contract.functions.slot0().call(block_identifier=block)[1]
        feeGrowthGlobal0 = pool_contract.functions.feeGrowthGlobal0X128().call(block_identifier=block)
        feeGrowthGlobal1 = pool_contract.functions.feeGrowthGlobal1X128().call(block_identifier=block)
        feeGrowthOutside0X128low = pool_contract.functions.ticks(lower_tick).call(block_identifier=block)[2]
        feeGrowthOutside1X128low = pool_contract.functions.ticks(lower_tick).call(block_identifier=block)[3]
        feeGrowthOutside0X128up = pool_contract.functions.ticks(upper_tick).call(block_identifier=block)[2]
        feeGrowthOutside1X128up = pool_contract.functions.ticks(upper_tick).call(block_identifier=block)[3]
        if current_tick >= lower_tick:
            fee_lower_token0 = feeGrowthOutside0X128low
            fee_lower_token1 = feeGrowthOutside1X128low
        else:
            fee_lower_token0 = feeGrowthGlobal0 - feeGrowthOutside0X128low
            fee_lower_token1 = feeGrowthGlobal1 - feeGrowthOutside1X128low
        if current_tick >= upper_tick:
            fee_upper_token0 = feeGrowthGlobal0 - feeGrowthOutside0X128up
            fee_upper_token1 = feeGrowthGlobal1 - feeGrowthOutside1X128up
        else:
            fee_upper_token0 = feeGrowthOutside0X128up
            fee_upper_token1 = feeGrowthOutside1X128up
        fee_growth_inside_last_0 = nft_positions[8]
        fee_growth_inside_last_1 = nft_positions[9]
        unclaimed_fees0 = int(Decimal(
            (feeGrowthGlobal0 - fee_lower_token0 - fee_upper_token0 - fee_growth_inside_last_0) * liquidity) / Decimal(
            2 ** 128))
        unclaimed_fees1 = int(Decimal(
            (feeGrowthGlobal1 - fee_lower_token1 - fee_upper_token1 - fee_growth_inside_last_1) * liquidity) / Decimal(
            2 ** 128))

        if decimals is True:
            decimals0 = get_decimals(token0, blockchain, web3=web3)
            decimals1 = get_decimals(token1, blockchain, web3=web3)
            unclaimed_fees0 = float(Decimal(unclaimed_fees0) / Decimal(10 ** decimals0))
            unclaimed_fees1 = float(Decimal(unclaimed_fees1) / Decimal(10 ** decimals1))

        fees.append([token0, unclaimed_fees0])
        fees.append([token1, unclaimed_fees1])
        return fees

    except GetNodeIndexError:
        return get_fee(nftid, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_fee(nftid, block, blockchain, index=index + 1, execution=execution)

# #to test
#wallet='0x849D52316331967b6fF1198e5E32A0eB168D039d'
#id = 339884
#uniswapv3 = underlying(wallet,id,'latest',ETHEREUM)
#print(uniswapv3)
#nfts_list = allnfts(wallet, 'latest', ETHEREUM)
#print(nfts_list)
#nfts = underlying_all(wallet,'latest',ETHEREUM)
#print(nfts)
#feesunclaimed = get_fee(wallet,id,'latest',ETHEREUM)
#print(feesunclaimed)