from pathlib import Path
import os
import json

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BLOCKCHAINS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ETHEREUM = 'ethereum'
POLYGON = 'polygon'
XDAI = 'xdai'
ARBITRUM = 'arbitrum'
BINANCE = 'binance'
AVALANCHE = 'avalanche'
FANTOM = 'fantom'
OPTIMISM = 'optimism'
AVAX = 'avax'
ROPSTEN = 'ropsten'
KOVAN = 'kovan'
GOERLI = 'goerli'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NODES
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# with open(str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/config.json', 'r') as config_file:
#         # Reading from json file
#         config_data = json.load(config_file)
#         config_file.close()

# NODE_ETH = {
#     'latest': config_data['nodes'][ETHEREUM]['latest'],
#     'archival': config_data['nodes'][ETHEREUM]['archival']
# }

# NODE_POL = {
#     'latest': config_data['nodes'][POLYGON]['latest'],
#     'archival': config_data['nodes'][POLYGON]['archival']
# }

# NODE_XDAI = {
#     'latest': config_data['nodes'][XDAI]['latest'],
#     'archival': config_data['nodes'][XDAI]['archival']
# }

# NODE_BINANCE = {
#     'latest': config_data['nodes'][BINANCE]['latest'],
#     'archival': config_data['nodes'][BINANCE]['archival']
# }

# NODE_AVALANCHE = {
#     'latest': config_data['nodes'][AVALANCHE]['latest'],
#     'archival': config_data['nodes'][AVALANCHE]['archival']
# }

# NODE_FANTOM = {
#     'latest': config_data['nodes'][FANTOM]['latest'],
#     'archival': config_data['nodes'][FANTOM]['archival']
# }

# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # TESTNETS
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NODE_ROPSTEN = {
#     'latest': config_data['nodes'][ROPSTEN]['latest'],
#     'archival': config_data['nodes'][ROPSTEN]['archival']
# }

# NODE_KOVAN = {
#     'latest': config_data['nodes'][KOVAN]['latest'],
#     'archival': config_data['nodes'][KOVAN]['archival']
# }

# NODE_GOERLI = {
#     'latest': config_data['nodes'][GOERLI]['latest'],
#     'archival': config_data['nodes'][GOERLI]['archival']
# }



NODE_ETH = {
    'latest': ['https://eth-mainnet.g.alchemy.com/v2/ki4i9jNJQvVOD51oXAa9RWK1tptcFFqV', 'https://eth-mainnet.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': ['https://eth-mainnet.g.alchemy.com/v2/ki4i9jNJQvVOD51oXAa9RWK1tptcFFqV', 'https://rpc.ankr.com/eth', 'https://eth-archival.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c', 'https://eth-mainnet.nodereal.io/v1/9f5c0354b11047cea3e9202de2c1eab0']
}

NODE_POL = {
    'latest': ['https://polygon-mainnet.g.alchemy.com/v2/AgULU1yvFJfC-QCT42MDcAtz6LfqTG4m','https://poly-mainnet.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c', 'https://polygon-rpc.com'],
    'archival': ['https://polygon-mainnet.g.alchemy.com/v2/AgULU1yvFJfC-QCT42MDcAtz6LfqTG4m', 'https://rpc.ankr.com/polygon', 'https://poly-archival.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c']
}

NODE_XDAI = {
    'latest': ['https://rpc.gnosischain.com/', 'https://gnosischain-rpc.gateway.pokt.network/', 'https://rpc.ankr.com/gnosis', 'https://gno.getblock.io/mainnet/?api_key=ec8f1352-32ad-4b35-a037-d899e5601b62', 'https://poa-xdai.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': ['https://rpc.ankr.com/gnosis', 'https://poa-xdai-archival.gateway.pokt.network/v1/lb/629a5a7050ec8c0039bbbc39', 'https://poa-xdai-archival.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c']
}

NODE_BINANCE = {
    'latest': ['https://bsc-dataseed.binance.org/', 'https://bsc-dataseed1.defibit.io/', 'https://bsc-dataseed1.ninicoin.io/', 'https://bsc-mainnet.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': ['https://bsc-mainnet.nodereal.io/v1/214197d3408f4bdda6568d5d414a59ae']
}

NODE_AVALANCHE = {
    'latest': ['https://avax-mainnet.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': ['https://api.avax.network/ext/bc/C/rpc', 'https://avax-archival.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c']
}

NODE_FANTOM = {
    'latest': ['https://rpc.ftm.tools/', 'https://fantom-mainnet.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': ['https://rpc.ankr.com/fantom']
}

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTNETS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
NODE_ROPSTEN = {
    'latest': ['https://eth-ropsten.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': []
}

NODE_KOVAN = {
    'latest': ['https://poa-kovan.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': []
}

NODE_GOERLI = {
    'latest': ['https://eth-goerli.gateway.pokt.network/v1/lb/629a5b7d50ec8c0039bbbf0c'],
    'archival': []
}


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAX EXECUTIONS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Maximum number of executions with different RPC endpoints, for a given function, in case of getting Unexpected Exceptions
MAX_EXECUTIONS = 2


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TESTNET HEADER
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Etherscan blocks requests that don't provide a User-Agent Hearder for Testnets.
TESTNET_HEADER = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36'}


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERC-20
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GENERAL
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ALL ZEROS ADDRESS
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
# ALL E ADDRESS
E_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
# ABI Token Simplified - name, symbol, decimals, balanceOf, totalSupply
ABI_TOKEN_SIMPLIFIED = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"}, {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM - Token Addresses
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AURA_ETH = '0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF'
B_80BAL_20_WETH_ETH = '0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56'
BAL_ETH = '0xba100000625a3754423978a60c9317c58a424e3D'
BB_A_USD_OLD_ETH = '0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2'
BB_A_USD_ETH = '0xA13a9247ea42D743238089903570127DdA72fE44'
COW_ETH = '0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB'
CRV_ETH = '0xD533a949740bb3306d119CC777fa900bA034cd52'
CRV_FRAX_ETH = '0x3175Df0976dFA876431C2E9eE6Bc45b65d3473CC'
CVX_ETH = '0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b'
CVXCRV_ETH = '0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7'
DAI_ETH = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
GNO_ETH = '0x6810e776880C02933D47DB1b9fc05908e5386b96'
STETH_ETH = '0xae7ab96520de3a18e5e111b5eaab095312d7fe84'
STK_AAVE_ETH = '0x4da27a545c0c5B758a6BA100e3a049001de870f5'
USDT_ETH = '0xdac17f958d2ee523a2206206994597c13d831ec7'
USDC_ETH = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
WETH_ETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
WSTETH_ETH = '0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0'
X3CRV_ETH = '0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# XDAI - Token Addresses
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AGVE_XDAI = '0x3a97704a1b25F08aa230ae53B352e2e72ef52843'
COW_XDAI = '0x177127622c4A00F3d409B75571e12cB3c8973d3c'
CRV_XDAI = '0x712b3d230F3C1c19db860d80619288b1F0BDd0Bd'
GNO_XDAI = '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb'
STK_AGAVE_XDAI = '0x610525b415c1BFAeAB1a3fc3d85D87b92f048221'
WETH_XDAI = '0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1'
X3CRV_XDAI = '0x1337BedC9D22ecbe766dF105c9623922A27963EC'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POLYGON - Token Addresses
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
BAL_POL = '0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3'
MAI_POL = '0xa3fa99a148fa48d14ed51d610c367c61876997f1'
X3CRV_POL = '0xE7a24EF0C5e95Ffb0f6684b813A78F2a3AD7D171'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# WALLETS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# DAO Wallets
WALLET_39D = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
WALLET_E6F = '0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f'
WALLET_7CC = '0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC'
WALLET_5F0 = '0x77bcb57ba7037e39063f1567ce734452bbD7a5F0'

# LTD Wallets
WALLET_462 = '0x4971DD016127F390a3EF6b956Ff944d0E2e1e462'
WALLET_8A3 = '0xe615bb53aC71e621167751FA5A9366E5D01D88a3'
WALLET_969 = '0x10E4597fF93cbee194F4879f8f1d54a370DB6969'

# KPK Wallets
WALLET_6E9 = '0x46f6B1D519a5bDaf10d49e135c9F611c9bd126e9'
WALLET_E1C = '0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C'
WALLET_A9A = '0x5FF85ECf773Ea3885Cb4b691068AB6d7BF8BDa9A'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOLS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
AAVE = 'Aave'
AGAVE = 'Agave'
AURA = 'Aura'
BALANCER = 'Balancer'
CONVEX = 'Convex'
CURVE = 'Curve'
ELK = 'Elk'
HONEYSWAP = 'Honeyswap'
MAKER = 'Maker'
QIDAO = 'QiDao'
SUSHISWAP = 'SushiSwap'
SWAPR = 'Swapr'
SYMMETRIC = 'Symmetric'
UNIT = 'Unit'


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# API KEYS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
API_KEY_ETHERSCAN = 'W1TK6XRQHME8X29PATD7YSXEHZ2QZJQPZE'
API_KEY_POLSCAN   = 'WQDQG6SJSURP8FPIYR6YZ5WWGTIUCZAXKY'
API_KEY_GNOSISSCAN = '3DS98QBPYWGYHT4KFQV8S4Q727GYBJ74YN'
API_KEY_BINANCE = 'QWYSFBURCYPH4QYT8BX277S436EVEFIIJI'
API_KEY_AVALANCHE = 'Z47JD79PBFFEUD6I6K5D4RB58WTGURPAAY'
API_KEY_FANTOM = 'N7EFVFCG7SBRIZZZWJ4VGC786JFAH8A3ZZ'

API_KEY_ETHPLORER = 'EK-qGMsQ-ghT7G9u-QsJLE'


# API_KEY_ETHERSCAN = config_data['apikeys']['etherscan']
# API_KEY_POLSCAN   = config_data['apikeys']['polscan']
# API_KEY_GNOSISSCAN = config_data['apikeys']['gnosisscan']
# API_KEY_BINANCE = config_data['apikeys']['binance']
# API_KEY_AVALANCHE = config_data['apikeys']['avalanche']
# API_KEY_FANTOM = config_data['apikeys']['fantom']

# API_KEY_ETHPLORER = config_data['apikeys']['ethplorer']

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# API CALLS
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COINGECKO
API_COINGECKO_COINID_PRICE_RANGE = 'https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=usd&from=%d&to=%d'
API_COINGECKO_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE = 'https://api.coingecko.com/api/v3/coins/%s/contract/%s/market_chart/range?vs_currency=usd&from=%d&to=%d'
API_COINGECKO_BLOCKCHAINID_TOKENADDRESS_PRICE = 'https://api.coingecko.com/api/v3/coins/%s/contract/%s'

# SCANS - MODULE = BLOCKS - GETBLOCKNOBYTIME
API_ETHERSCAN_GETBLOCKNOBYTIME = 'https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_POLYGONSCAN_GETBLOCKNOBYTIME = 'https://api.polygonscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_GNOSISSCAN_GETBLOCKNOBYTIME = 'https://api.gnosisscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_BLOCKSCOUT_GETBLOCKNOBYTIME = 'https://blockscout.com/xdai/mainnet/api?module=block&action=getblocknobytime&timestamp=%d&closest=before'
API_BINANCE_GETBLOCKNOBYTIME = 'https://api.bscscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_AVALANCHE_GETBLOCKNOBYTIME = 'https://api.snowtrace.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_FANTOM_GETBLOCKNOBYTIME = 'https://api.ftmscan.com/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_ROPSTEN_GETBLOCKNOBYTIME = 'https://api-ropsten.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_KOVAN_GETBLOCKNOBYTIME = 'https://api-kovan.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'
API_GOERLI_GETBLOCKNOBYTIME = 'https://api-goerli.etherscan.io/api?module=block&action=getblocknobytime&timestamp=%d&closest=before&apikey=%s'

# SCANS - MODULE = BLOCKS - GETBLOCKREWARD
API_ETHERSCAN_GETBLOCKREWARD = 'https://api.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_POLYGONSCAN_GETBLOCKREWARD = 'https://api.polygonscan.com/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_GNOSISSCAN_GETBLOCKREWARD = 'https://api.gnosisscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_BLOCKSCOUT_GETBLOCKREWARD = 'https://blockscout.com/xdai/mainnet/api?module=block&action=getblockreward&blockno=%d'
API_BINANCE_GETBLOCKREWARD = 'https://api.bscscan.com/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_AVALANCHE_GETBLOCKREWARD = 'https://api.snowtrace.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_ROPSTEN_GETBLOCKREWARD = 'https://api-ropsten.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_KOVAN_GETBLOCKREWARD = 'https://api-kovan.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'
API_GOERLI_GETBLOCKREWARD = 'https://api-goerli.etherscan.io/api?module=block&action=getblockreward&blockno=%d&apikey=%s'

# SCANS - MODULE = CONTRACTS - GETABI
API_ETHERSCAN_GETABI = 'https://api.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s'
API_POLYGONSCAN_GETABI = 'https://api.polygonscan.com/api?module=contract&action=getabi&address=%s&apikey=%s'
API_GNOSISSCAN_GETABI = 'https://api.gnosisscan.io/api?module=contract&action=getabi&address=%s&apikey=%s'
API_BLOCKSCOUT_GETABI = 'https://blockscout.com/xdai/mainnet/api?module=contract&action=getabi&address=%s'
API_BINANCE_GETABI = 'https://api.bscscan.com/api?module=contract&action=getabi&address=%s&apikey=%s'
API_ROPSTEN_GETABI = 'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s'
API_KOVAN_GETABI = 'https://api-kovan.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s'
API_GOERLI_GETABI = 'https://api-goerli.etherscan.io/api?module=contract&action=getabi&address=%s&apikey=%s'

# SCANS - MODULE = ACCOUNTS - TOKENTX
API_ETHERSCAN_TOKENTX = 'https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_POLYGONSCAN_TOKENTX = 'https://api.polygonscan.com/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_GNOSISSCAN_TOKENTX = 'https://api.gnosisscan.io/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_BLOCKSCOUT_TOKENTX = 'https://blockscout.com/xdai/mainnet/api?module=account&action=tokentx&contractaddress=%s&address=%s&startblock=%s&endblock=%s&sort=desc'

# SCANS - MODULE = ACCOUNTS - TXLIST
API_ETHERSCAN_TXLIST = 'https://api.etherscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_POLYGONSCAN_TXLIST = 'https://api.polygonscan.com/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_GNOSISSCAN_TXLIST = 'https://api.gnosisscan.io/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc&apikey=%s'
API_BLOCKSCOUT_TXLIST = 'https://blockscout.com/xdai/mainnet/api?module=account&action=txlist&address=%s&startblock=%s&endblock=%s&sort=desc'

# SCANS - MODULE = LOGS - GETLOGS
API_ETHERSCAN_GETLOGS = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'
API_POLYGONSCAN_GETLOGS = 'https://api.polygonscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'
API_GNOSISSCAN_GETLOGS = 'https://api.gnosisscan.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'
API_BLOCKSCOUT_GETLOGS = 'https://blockscout.com/xdai/mainnet/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s'
API_AVALANCHE_GETLOGS = 'https://api.snowtrace.io/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'
API_BINANCE_GETLOGS = 'https://api.bscscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'
API_FANTOM_GETLOGS = 'https://api.ftmscan.com/api?module=logs&action=getLogs&fromBlock=%s&toBlock=%s&address=%s&topic0=%s&apikey=%s'

# TOKEN INFO
API_ETHPLORER_GETTOKENINFO = 'https://api.ethplorer.io/getTokenInfo/%s?apiKey=%s'
API_BLOCKSCOUT_GETTOKENCONTRACT = 'https://blockscout.com/xdai/mainnet/api?module=token&action=getToken&contractaddress=%s'
