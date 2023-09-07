from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby
from operator import itemgetter
from typing import Union

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defi_protocols.cache import const_call
from defi_protocols.constants import (
    ARBITRUM,
    ETHEREUM,
    OPTIMISM,
    POLYGON,
    XDAI,
    ZERO_ADDRESS,
    ArbitrumTokenAddr,
    ETHTokenAddr,
    GnosisTokenAddr,
    OptimismTokenAddr,
    PolygonTokenAddr,
)
from defi_protocols.functions import (
    balance_of,
    block_to_date,
    date_to_block,
    get_contract,
    get_decimals,
    get_logs_web3,
    get_node,
    last_block,
    to_token_amount,
)
from defi_protocols.prices.prices import get_price

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BALANCER VAULT
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault Contract Address
VAULT = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LIQUIDITY GAUGE FACTORY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ETHEREUM = "0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_ETHEREUM_V2 = "0xf1665E19bc105BE4EDD3739F88315cC699cc5b65"

# Polygon Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_POLYGON = "0x3b8cA519122CdD8efb272b0D3085453404B25bD0"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_POLYGON_V2 = "0x22625eEDd92c81a219A83e1dc48f88d54786B017"

# Arbitrum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ARBITRUM = "0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_ARBITRUM_V2 = "0x6817149cb753BF529565B4D023d7507eD2ff4Bc0"

# GC Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_XDAI = "0x809B79b53F18E9bc08A961ED4678B901aC93213a"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_XDAI_V2 = "0x83E443EF4f9963C77bd860f94500075556668cb8"

# Optimism Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_OPTIMISM = "0x2E96068b3D5B5BAE3D7515da4A1D2E52d08A2647"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_OPTIMISM_V2 = "0x83E443EF4f9963C77bd860f94500075556668cb8"

# This dict holds the block in which each deployed Liquidity Gauge Factory was created
GAUGE_FACTORIES = {
    ETHEREUM: {"14457664": LIQUIDITY_GAUGE_FACTORY_ETHEREUM, "15399251": LIQUIDITY_GAUGE_FACTORY_ETHEREUM_V2},
    POLYGON: {"27098624": LIQUIDITY_GAUGE_FACTORY_POLYGON, "40687417": LIQUIDITY_GAUGE_FACTORY_POLYGON_V2},
    ARBITRUM: {"9756975": LIQUIDITY_GAUGE_FACTORY_ARBITRUM, "72942741": LIQUIDITY_GAUGE_FACTORY_ARBITRUM_V2},
    XDAI: {"26615210": LIQUIDITY_GAUGE_FACTORY_XDAI, "27088528": LIQUIDITY_GAUGE_FACTORY_XDAI_V2},
    OPTIMISM: {"60740": LIQUIDITY_GAUGE_FACTORY_OPTIMISM, "641824": LIQUIDITY_GAUGE_FACTORY_OPTIMISM_V2},
}


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL Contract Address
VEBAL = "0xC128a9954e6c874eA3d62ce62B468bA073093F25"

# veBAL Fee Distributor Contract
VEBAL_FEE_DISTRIBUTOR = "0x26743984e3357eFC59f2fd6C1aFDC310335a61c9"  # DEPRECATED
VEBAL_FEE_DISTRIBUTOR_V2 = "0xD3cf852898b21fc233251427c2DC93d3d604F3BB"

VEBAL_FEE_DISTRIBUTORS = {
    "14623899": VEBAL_FEE_DISTRIBUTOR,
    "15149500": VEBAL_FEE_DISTRIBUTOR_V2,
}

# veBAL Reward Tokens - BAL, bb-a-USD old deployment, bb-a-USD, bb-a-USDv3
VEBAL_REWARD_TOKENS = {
    "14623899": [ETHTokenAddr.BAL, ETHTokenAddr.BB_A_USD_OLD, ETHTokenAddr.BB_A_USD],
    "16981440": [
        ETHTokenAddr.BAL,
        ETHTokenAddr.BB_A_USD_OLD,
        ETHTokenAddr.BB_A_USD,
        ETHTokenAddr.BB_A_USD_V3,
        ETHTokenAddr.USDC,
    ],
}

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHILD CHAIN GAUGE REWARD HELPER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GC Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_XDAI = "0xf7D5DcE55E6D47852F054697BAB6A1B48A00ddbd"

# Polygon Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_POLYGON = "0xaEb406b0E430BF5Ea2Dc0B9Fe62E4E53f74B3a33"

# Arbitrum Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_ARBITRUM = "0xA0DAbEBAAd1b243BBb243f933013d560819eB66f"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault ABI - getPoolTokens, getPool
ABI_VAULT = '[{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"enum IVault.PoolSpecialization","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Liquidity Gauge Factory ABI - getPoolGauge
ABI_LIQUIDITY_GAUGE_FACTORY = '[{"inputs":[{"internalType":"address","name":"pool","type":"address"}],"name":"getPoolGauge","outputs":[{"internalType":"contract ILiquidityGauge","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# veBAL ABI - locked, token
ABI_VEBAL = '[{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"locked","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"amount","type":"int128"},{"name":"end","type":"uint256"}]}]}]'

# veBAL Fee Distributor ABI - claimTokens
ABI_VEBAL_FEE_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"claimTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]'

# LP Token ABI - getPoolId, decimals, getActualSupply, getVirtualSupply, totalSupply, getBptIndex, balanceOf, getSwapFeePercentage, getRate, getScalingFactors, POOL_ID
ABI_LPTOKEN = '[{"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getActualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getVirtualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getBptIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getSwapFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getScalingFactors","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"POOL_ID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

# Gauge ABI - claimable_tokens, claimable_reward, reward_count, reward_tokens, reward_contract
ABI_GAUGE = '[{"stateMutability":"nonpayable","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"claimable_reward","inputs":[{"name":"_user","type":"address"},{"name":"_reward_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"reward_contract","inputs":[],"outputs":[{"name":"","type":"address"}]}]'

# ABI Pool Tokens - decimals, getRate, UNDERLYING_ASSET_ADDRESS, rate, stETH, UNDERLYING
ABI_POOL_TOKENS_BALANCER = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMainToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"stETH","outputs":[{"internalType":"contract IStETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"UNDERLYING","outputs":[{"internalType":"contract IERC20Upgradeable","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

# ABI Child Gauge Reward Helper - getPendingRewards
ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER = '[{"inputs":[{"internalType":"contract IRewardsOnlyGauge","name":"gauge","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"token","type":"address"}],"name":"getPendingRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]'

# ABI Child Chain Streamer - reward_count
ABI_CHILD_CHAIN_STREAMER = '[{"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(bytes32,address,address,uint256,uint256)"

# Gauge Created Event Signature
GAUGE_CREATED_EVENT_SIGNATURE = "GaugeCreated(address)"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# call_contract_method
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def call_contract_method(method, block):
    try:
        return method.call(block_identifier=block)
    except Exception as e:
        if (
            type(e) == ContractLogicError
            or type(e) == BadFunctionCallOutput
            or (type(e) == ValueError and (e.args[0]["code"] == -32000 or e.args[0]["code"] == -32015))
        ):
            return None
        else:
            raise e


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_gauge_addresses
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gauge_addresses(blockchain, block, web3, lptoken_addr):
    if isinstance(block, str):
        if block == "latest":
            block = last_block(blockchain)
        else:
            raise ValueError("Incorrect block.")

    gauge_addresses = []

    blocks = list(GAUGE_FACTORIES[blockchain].keys())[::-1]
    for iblock in blocks:
        gauge_address = ZERO_ADDRESS
        if block >= int(iblock):
            gauge_factory_address = GAUGE_FACTORIES[blockchain][iblock]

            if iblock == blocks[-1]:
                gauge_factory_contract = get_contract(
                    gauge_factory_address, blockchain, web3=web3, abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block
                )
                gauge_address = call_contract_method(gauge_factory_contract.functions.getPoolGauge(lptoken_addr), block)
                if gauge_address != ZERO_ADDRESS:
                    gauge_addresses.append(Web3.to_checksum_address(gauge_address))
            else:
                block_from = int(iblock)
                gauge_created_event = web3.keccak(text=GAUGE_CREATED_EVENT_SIGNATURE).hex()

                if block >= block_from:
                    logs = get_logs_web3(
                        blockchain=blockchain,
                        address=gauge_factory_address,
                        block_start=block_from,
                        block_end=block,
                        topics=[gauge_created_event],
                        web3=web3,
                    )
                    for log in logs:
                        tx = web3.eth.get_transaction(log["transactionHash"])
                        # For some endpoints tx["input"] is a string and for others is a bytes object
                        input = tx["input"].hex() if isinstance(tx["input"], bytes) else tx["input"]
                        if lptoken_addr[2 : len(lptoken_addr)].lower() in input:
                            gauge_address = Web3.to_checksum_address(f"0x{log['topics'][1].hex()[-40:]}")
                            break

                if gauge_address == ZERO_ADDRESS:
                    continue
                else:
                    gauge_addresses.append(gauge_address)

    return gauge_addresses


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# is_meta_pool
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def is_meta_pool(web3, vault_contract, bpt_index, pool_id, block, blockchain):
    pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)
    pool_tokens = pool_tokens_data[0]

    is_meta = True
    for i in range(len(pool_tokens)):
        if i == bpt_index:
            continue

        token_address = pool_tokens[i]
        token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block)

        if call_contract_method(token_contract.functions.getPoolId(), block) is None:
            is_meta = False
            break

    return is_meta


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    try:
        lptoken_data["poolId"] = const_call(lptoken_data["contract"].functions.getPoolId())
    except ContractLogicError:
        try:
            lptoken_data["poolId"] = const_call(lptoken_data["contract"].functions.POOL_ID())
        except ContractLogicError:
            lptoken_data["poolId"] = None

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())

    try:
        lptoken_data["totalSupply"] = lptoken_data["contract"].functions.getActualSupply().call(block_identifier=block)
    except:
        try:
            lptoken_data["totalSupply"] = (
                lptoken_data["contract"].functions.getVirtualSupply().call(block_identifier=block)
            )
        except:
            lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)

    try:
        lptoken_data["bptIndex"] = const_call(lptoken_data["contract"].functions.getBptIndex())
    except:
        lptoken_data["bptIndex"] = None

    try:
        lptoken_data["scalingFactors"] = (
            lptoken_data["contract"].functions.getScalingFactors().call(block_identifier=block)
        )
    except:
        lptoken_data["scalingFactors"] = None

    return lptoken_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_address(blockchain):
    if blockchain == ETHEREUM:
        return ETHTokenAddr.BAL
    elif blockchain == POLYGON:
        return PolygonTokenAddr.BAL
    elif blockchain == ARBITRUM:
        return ArbitrumTokenAddr.BAL
    elif blockchain == XDAI:
        return GnosisTokenAddr.BAL
    elif blockchain == OPTIMISM:
        return OptimismTokenAddr.BAL


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_child_chain_reward_helper_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_child_chain_reward_helper_address(blockchain):
    if blockchain == XDAI:
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_XDAI
    elif blockchain == POLYGON:
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_POLYGON
    elif blockchain == ARBITRUM:
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_ARBITRUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_rewards(web3, gauge_addresses, wallet, block, blockchain, decimals=True):
    bal_rewards = Decimal(0)
    for gauge_address in gauge_addresses:
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)
        bal_address = get_bal_address(blockchain)
        bal_rewards_aux = call_contract_method(gauge_contract.functions.claimable_tokens(wallet), block)
        if bal_rewards_aux is None:
            bal_rewards_aux = call_contract_method(
                gauge_contract.functions.claimable_reward(wallet, bal_address), block
            )

        if bal_rewards_aux is not None:
            bal_rewards += bal_rewards_aux

    return [bal_address, to_token_amount(bal_address, bal_rewards, blockchain, web3, decimals)]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, gauge_addresses, wallet, block, blockchain, decimals=True):
    rewards = []
    rewards_dict = {}

    for gauge_address in gauge_addresses:
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)
        reward_count = call_contract_method(gauge_contract.functions.reward_count(), block) or 0

        for i in range(reward_count):
            token_address = const_call(gauge_contract.functions.reward_tokens(i))

            if blockchain == ETHEREUM:
                token_rewards = gauge_contract.functions.claimable_reward(wallet, token_address).call(
                    block_identifier=block
                )
            else:
                child_chain_reward_helper_contract = get_contract(
                    get_child_chain_reward_helper_address(blockchain),
                    blockchain,
                    web3=web3,
                    abi=ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER,
                    block=block,
                )
                token_rewards = child_chain_reward_helper_contract.functions.getPendingRewards(
                    gauge_address, wallet, token_address
                ).call(block_identifier=block)

            if token_address in rewards_dict.keys():
                rewards_dict[token_address] += to_token_amount(token_address, token_rewards, blockchain, web3, decimals)
            else:
                rewards_dict[token_address] = to_token_amount(token_address, token_rewards, blockchain, web3, decimals)

    rewards = list(map(list, rewards_dict.items()))

    return rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vebal_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vebal_rewards(web3, wallet, block, blockchain, decimals=True):
    if isinstance(block, str):
        if block == "latest":
            block = last_block(blockchain)
        else:
            raise ValueError("Incorrect block.")

    vebal_rewards = []
    vebal_rewards_dict = {}

    fee_distributor_blocks = list(VEBAL_FEE_DISTRIBUTORS.keys())[::-1]
    # Continues only if the block is greater than the first fee distributor block
    if block >= int(fee_distributor_blocks[-1]):
        vebal_reward_tokens_blocks = list(VEBAL_REWARD_TOKENS.keys())

        i = 0
        # Obtains the block to determine the reward tokens
        while i < len(vebal_reward_tokens_blocks):
            if block >= int(vebal_reward_tokens_blocks[i]):
                vebal_reward_tokens_block = vebal_reward_tokens_blocks[i]
            i += 1

        for fee_distributor_block in fee_distributor_blocks:
            if block >= int(fee_distributor_block):
                fee_distributor_contract = get_contract(
                    VEBAL_FEE_DISTRIBUTORS[fee_distributor_block],
                    blockchain,
                    web3=web3,
                    abi=ABI_VEBAL_FEE_DISTRIBUTOR,
                    block=block,
                )
                claim_tokens = fee_distributor_contract.functions.claimTokens(
                    wallet, VEBAL_REWARD_TOKENS[vebal_reward_tokens_block]
                ).call(block_identifier=block)

                for i in range(len(VEBAL_REWARD_TOKENS[vebal_reward_tokens_block])):
                    token_address = VEBAL_REWARD_TOKENS[vebal_reward_tokens_block][i]
                    token_rewards = claim_tokens[i]
                    if token_address in vebal_rewards_dict.keys():
                        vebal_rewards_dict[token_address] += to_token_amount(
                            token_address, token_rewards, blockchain, web3, decimals
                        )
                    else:
                        vebal_rewards_dict[token_address] = to_token_amount(
                            token_address, token_rewards, blockchain, web3, decimals
                        )

    vebal_rewards = list(map(list, vebal_rewards_dict.items()))

    return vebal_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, gauge_addresses=None):
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if gauge_addresses is None:
        gauge_addresses = get_gauge_addresses(blockchain, block, web3, lptoken_address)

    # veBAL Rewards
    if blockchain == ETHEREUM:
        vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

        if lptoken_address == const_call(vebal_contract.functions.token()):
            vebal_rewards = get_vebal_rewards(web3, wallet, block, blockchain, decimals=decimals)

            if len(vebal_rewards) > 0:
                for vebal_reward in vebal_rewards:
                    all_rewards.append(vebal_reward)

    if gauge_addresses != []:
        bal_rewards = get_bal_rewards(web3, gauge_addresses, wallet, block, blockchain)
        all_rewards.append(bal_rewards)

        rewards = get_rewards(web3, gauge_addresses, wallet, block, blockchain)

        if len(rewards) > 0:
            for reward in rewards:
                all_rewards.append(reward)

    return all_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, reward=False, aura_staked=None, decimals=True):
    result = []
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    gauge_addresses = get_gauge_addresses(blockchain, block, web3, lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)
    lptoken_data["balanceOf"] = Decimal(
        lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)
    )

    pool_staked_fraction = Decimal(0)
    for gauge_address in gauge_addresses:
        lptoken_data["staked"] = balance_of(wallet, gauge_address, block, blockchain, web3=web3, decimals=False)
        pool_staked_fraction += lptoken_data["staked"] / lptoken_data["totalSupply"]

    lptoken_data["locked"] = Decimal(0)
    if blockchain == ETHEREUM:
        vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

        if lptoken_address == const_call(vebal_contract.functions.token()):
            try:
                lptoken_data["locked"] = Decimal(
                    vebal_contract.functions.locked(wallet).call(block_identifier=block)[0]
                )
            except:
                pass

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        pool_balance_fraction = lptoken_data["balanceOf"] / lptoken_data["totalSupply"]
        pool_locked_fraction = lptoken_data["locked"] / lptoken_data["totalSupply"]
        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []

            if call_contract_method(token_contract.functions.getPoolId(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / (10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address

                if lptoken_data["scalingFactors"] is not None and is_meta_pool(
                    web3, vault_contract, lptoken_data["bptIndex"], lptoken_data["poolId"], block, blockchain
                ):
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / (10 ** (2 * 18 - token_decimals))
                    )
                else:
                    token_balance = pool_balances[i]

                if decimals is True:
                    token_balance = token_balance / (10**token_decimals)

                unwrapped_balances.append([main_token, token_balance])

            for main_token, token_balance in unwrapped_balances:
                token_balance = Decimal(token_balance)

                if aura_staked is None:
                    token_staked = token_balance * pool_staked_fraction
                else:
                    aura_pool_fraction = Decimal(aura_staked) / lptoken_data["totalSupply"]
                    token_staked = token_balance * aura_pool_fraction

                token_locked = token_balance * pool_locked_fraction
                token_balance = token_balance * pool_balance_fraction

                balances.append([main_token, token_balance, token_staked, token_locked])

        if reward is True:
            all_rewards = get_all_rewards(
                wallet,
                lptoken_address,
                block,
                blockchain,
                web3=web3,
                decimals=decimals,
                gauge_addresses=gauge_addresses,
            )

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []
            if call_contract_method(token_contract.functions.getPoolId(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / Decimal(10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address

                if lptoken_data["scalingFactors"] is not None and is_meta_pool(
                    web3, vault_contract, lptoken_data["bptIndex"], lptoken_data["poolId"], block, blockchain
                ):
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / Decimal(10 ** (2 * 18 - token_decimals))
                    )
                else:
                    main_token = pool_tokens[i]
                    token_balance = pool_balances[i]

                unwrapped_balances.append(
                    [main_token, to_token_amount(main_token, token_balance, blockchain, web3, decimals)]
                )

            for main_token, token_balance in unwrapped_balances:
                balances.append([main_token, token_balance])

        first = itemgetter(0)
        balances = [[k, sum(item[1] for item in tups_to_sum)] for k, tups_to_sum in groupby(balances, key=first)]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(
    lptoken_amount: Decimal,
    lptoken_address: str,
    block: int | str,
    blockchain: str,
    web3: Web3 = None,
    decimals: bool = True,
) -> Decimal:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        pool_balance_fraction = (
            Decimal(lptoken_amount) * Decimal(10 ** lptoken_data["decimals"]) / lptoken_data["totalSupply"]
        )

        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []
            if call_contract_method(token_contract.functions.getPoolId(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / Decimal(10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address

                if lptoken_data["scalingFactors"] is not None and is_meta_pool(
                    web3, vault_contract, lptoken_data["bptIndex"], lptoken_data["poolId"], block, blockchain
                ):
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / (10 ** (2 * 18 - token_decimals))
                    )
                else:
                    token_balance = pool_balances[i]

                if decimals is True:
                    token_balance = token_balance / (10**token_decimals)

                unwrapped_balances.append([main_token, token_balance])

            for unwrapped_balance in unwrapped_balances:
                main_token, token_balance = unwrapped_balance
                token_balance = token_balance * pool_balance_fraction

                balances.append([main_token, token_balance])

        first = itemgetter(0)
        balances = [[k, sum(item[1] for item in tups_to_sum)] for k, tups_to_sum in groupby(balances, key=first)]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    result = {}

    if web3 is None:
        web3 = get_node(blockchain, block=block_end)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)
    try:
        pool_id = const_call(lptoken_contract.functions.getPoolId())
    except ContractLogicError:
        try:
            pool_id = const_call(lptoken_contract.functions.POOL_ID())
        except ContractLogicError:
            pool_id = None

    if pool_id is not None:
        pool_id = "0x" + pool_id.hex()
        result["swaps"] = []
        swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()
        swap_logs = get_logs_web3(
            blockchain=blockchain,
            address=VAULT,
            block_start=block_start,
            block_end=block_end,
            topics=[swap_event, pool_id],
        )

        for swap_log in swap_logs:
            token_in = Web3.to_checksum_address(f"0x{swap_log['topics'][2].hex()[-40:]}")
            lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
            swap_fee = Decimal(
                lptoken_contract.functions.getSwapFeePercentage().call(block_identifier=swap_log["blockNumber"])
            )
            swap_fee /= Decimal(10**lptoken_decimals)
            swap_fee *= int(swap_log["data"].hex()[2:66], 16)

            swap_data = {
                "block": swap_log["blockNumber"],
                "tokenIn": token_in,
                "amountIn": to_token_amount(token_in, swap_fee, blockchain, web3, decimals),
            }

            result["swaps"].append(swap_data)

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_swap_fees_APR
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_swap_fees_APR(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> Decimal:
    block_start = date_to_block(
        datetime.strftime(
            datetime.strptime(block_to_date(block_end, blockchain), "%Y-%m-%d %H:%M:%S") - timedelta(days=days),
            "%Y-%m-%d %H:%M:%S",
        ),
        blockchain,
    )

    fees = swap_fees(lptoken_address, block_start, block_end, blockchain, web3)
    # create a dictionary to store the total amountIn for each tokenIn
    totals_dict = {}

    for swap in fees["swaps"]:
        token_in = swap["tokenIn"]
        amount_in = swap["amountIn"]
        if token_in in totals_dict:
            totals_dict[token_in] += amount_in
        else:
            totals_dict[token_in] = amount_in

    totals_list = [(token_in, amount_in) for token_in, amount_in in totals_dict.items()]

    fee = 0
    for k in totals_list:
        fee += k[1] * Decimal(get_price(k[0], block_end, blockchain, web3)[0])
    pool_balance = pool_balances(lptoken_address, block_end, blockchain)
    tvl = 0
    for balance in pool_balance:
        tvl += balance[1] * Decimal(get_price(balance[0], block_end, blockchain, web3)[0])

    rate = Decimal(fee / tvl)
    apr = (((1 + rate) ** Decimal(365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        return (1 + (apr / seconds_per_year)) ** seconds_per_year - 1
    else:
        return apr
