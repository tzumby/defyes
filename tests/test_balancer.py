import pytest

from defi_protocols import Balancer
from defi_protocols.constants import ETHEREUM, POLYGON, BAL_POL, ETHTokenAddr
from defi_protocols.functions import get_contract, get_node, date_to_block


WALLET_N1 = '0x31cD267D34EC6368eac930Be4f412dfAcc71A844'
WALLET_N2 = '0x4b0429F3db75dbA6B82c32a200C9C298ffC05839'
WALLET_N3 = '0xe8fAF95AD24A467ddDc4e100a68398B31D3dCdd6'
WALLET_N4 = '0x64aE36eeaC5BF9c1F4b7Cc6F0Fa32bBa19aaF9Bc'
WALLET_N5 = '0xce88686553686DA562CE7Cea497CE749DA109f9F'
WALLET_N6 = '0x43b650399F2E4D6f03503f44042fabA8F7D73470'
WALLET_39d = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
B60WETH40DAI_ADDR = '0x0b09deA16768f0799065C475bE02919503cB2a35'
B50USDC50WETH_ADDR = '0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8'
B80BAL20WETH_ADDR = '0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56'
BstETHSTABLE_ADDR = '0x32296969Ef14EB0c6d29669C550D4a0449130230'
B50wstETH50LDO_ADDR = '0x5f1f4e50ba51d723f12385a8a9606afc3a0555f5'
bbaUSD_ADDR = '0xA13a9247ea42D743238089903570127DdA72fE44'
bbaUSDT_ADDR = '0x2f4eb100552ef93840d5adc30560e5513dfffacb'
bbaUSDC_ADDR = '0x82698aecc9e28e9bb27608bd52cf57f704bd1b83'
bbaDAI_ADDR = '0xae37d54ae477268b9997d4161b96b8200755935c'


def test_get_gauge_factory_address():
    gauge_address = Balancer.get_gauge_factory_address(ETHEREUM)
    assert Balancer.LIQUIDITY_GAUGE_FACTORY_ETHEREUM == gauge_address


def test_get_bal_address():
    assert ETHTokenAddr.BAL == Balancer.get_bal_address(ETHEREUM)
    assert BAL_POL == Balancer.get_bal_address(POLYGON)


def test_get_lptoken_data():
    block = 16950590

    lptoken_data = Balancer.get_lptoken_data(B60WETH40DAI_ADDR, block, ETHEREUM)
    assert list(lptoken_data.keys()) == ['contract', 'poolId', 'decimals', 'totalSupply', 'isBoosted', 'bptIndex', 'scalingFactors', 'wrappedIndex']
    assert lptoken_data['poolId'] == b'\x0b\t\xde\xa1gh\xf0y\x90e\xc4u\xbe\x02\x91\x95\x03\xcb*5\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a'
    assert lptoken_data['decimals'] == 18
    assert lptoken_data['totalSupply'] == 12835022143788475405205
    assert not lptoken_data['isBoosted']
    assert lptoken_data['bptIndex'] is None
    assert lptoken_data['scalingFactors'] is None
    assert lptoken_data['wrappedIndex'] is None

    lptoken_data = Balancer.get_lptoken_data(bbaUSD_ADDR, block, ETHEREUM)
    assert lptoken_data['poolId'] == b'\xa1:\x92G\xeaB\xd7C#\x80\x89\x905p\x12}\xdar\xfeD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03]'
    assert lptoken_data['decimals'] == 18
    assert lptoken_data['totalSupply'] == 45626173875220118192194148
    assert lptoken_data['isBoosted']
    assert lptoken_data['bptIndex'] == 2
    assert lptoken_data['scalingFactors'] == [1008896757769783573, 1003250365192438010, 1000000000000000000, 1002548558018035032]
    assert lptoken_data['wrappedIndex'] is None

def test_bal_rewards():
    block = 16978206
    node = get_node(ETHEREUM, block)

    gauge_address = Balancer.get_gauge_address(ETHEREUM, block, node, B60WETH40DAI_ADDR)
    gauge_contract = get_contract(gauge_address,
                                  ETHEREUM,
                                  web3=node,
                                  abi=Balancer.ABI_GAUGE,
                                  block=block)

    bal_rewards = Balancer.get_bal_rewards(node, gauge_contract, WALLET_N1, block, ETHEREUM)
    assert bal_rewards[0] == ETHTokenAddr.BAL
    assert bal_rewards[1] == 1.267800098374e-06


def test_vebal_rewards():
    block = 16950590
    node = get_node(ETHEREUM, block)

    vebal_rewards = Balancer.get_vebal_rewards(node, WALLET_N2, block, ETHEREUM)
    assert vebal_rewards[0] == [ETHTokenAddr.BAL, 1.9372013715193e-05]
    assert vebal_rewards[1] == [ETHTokenAddr.BB_A_USD_OLD, 0.0]
    assert vebal_rewards[2] == [ETHTokenAddr.BB_A_USD, 0.000210261212072964]

    no_vebal_rewards = Balancer.get_vebal_rewards(node, WALLET_N1, block, ETHEREUM)
    for vebal_token in no_vebal_rewards:
        assert vebal_token[1] == 0


def test_get_rewards():
    block = 16978206
    node = get_node(ETHEREUM, block)

    gauge_address = Balancer.get_gauge_address(ETHEREUM, block, node, BstETHSTABLE_ADDR)
    gauge_contract = get_contract(gauge_address,
                                  ETHEREUM,
                                  web3=node,
                                  abi=Balancer.ABI_GAUGE,
                                  block=block)

    rewards = Balancer.get_rewards(node, gauge_contract, WALLET_N3, block, ETHEREUM)
    assert len(rewards) == 1

    ldo_reward = rewards[0]
    assert ldo_reward[0] == ETHTokenAddr.LDO
    assert ldo_reward[1] == 0


def test_all_rewards():
    block = 16978206
    node = get_node(ETHEREUM, block)

    all_rewards = Balancer.get_all_rewards(WALLET_N2, B50USDC50WETH_ADDR, block, ETHEREUM, node)
    assert all_rewards[0] == [ETHTokenAddr.BAL, 0.002255938639324377]

    all_rewards = Balancer.get_all_rewards(WALLET_N2, B80BAL20WETH_ADDR, block, ETHEREUM, node)
    assert all_rewards[0] == [ETHTokenAddr.BAL, 1.9372013715193e-05]
    assert all_rewards[1] == [ETHTokenAddr.BB_A_USD_OLD, 0.0]
    assert all_rewards[2] == [ETHTokenAddr.BB_A_USD, 0.000210261212072964]


def test_underlying():
    block = 16978206
    node = get_node(ETHEREUM, block)

    dai, weth = Balancer.underlying(WALLET_N1, B60WETH40DAI_ADDR, block, ETHEREUM, web3=node)
    # [token, balance, staked, locked]
    assert dai == [ETHTokenAddr.DAI, 0, 0.40645247675856844, 0]
    assert weth == [ETHTokenAddr.WETH, 0, 0.00032498828745960426, 0]

    tokens, rewards = Balancer.underlying(WALLET_N2, B50USDC50WETH_ADDR, block, ETHEREUM, web3=node, reward=True)
    usdc, weth = tokens
    # [token, balance, staked, locked]
    assert usdc == [ETHTokenAddr.USDC, 10.2460828145437, 10.589629665637453, 0]
    assert weth == [ETHTokenAddr.WETH, 0.00545880690641515, 0.005641838408050662, 0]

    bal_rewards = rewards[0]
    assert bal_rewards == [ETHTokenAddr.BAL, 0.002255938639324377]

    tokens, rewards = Balancer.underlying(WALLET_N2, B80BAL20WETH_ADDR, block, ETHEREUM, web3=node, reward=True)
    bal, weth = tokens
    # [token, balance, staked, locked]
    assert bal == [ETHTokenAddr.BAL, 0, 0, 1.0001144686226011]
    assert weth == [ETHTokenAddr.WETH, 0, 0, 0.0009405381335007069]

    bal, bb_a_usd_old, bb_a_usd = rewards
    assert bal == [ETHTokenAddr.BAL, 1.9372013715193e-05]
    assert bb_a_usd_old == [ETHTokenAddr.BB_A_USD_OLD, 0.0]
    assert bb_a_usd == [ETHTokenAddr.BB_A_USD, 0.000210261212072964]

def test_underlying2():
    block = 17117344
    node = get_node(ETHEREUM, block)

    steth, weth = Balancer.underlying(WALLET_N4, BstETHSTABLE_ADDR, block, ETHEREUM, web3=node)
    # [token, balance, staked, locked]
    assert steth == [ETHTokenAddr.stETH, 11.372321151072452, 0, 0]
    assert weth == [ETHTokenAddr.WETH, 10.939145284307902, 0, 0]

    ldo, wsteth = Balancer.underlying(WALLET_N5, B50wstETH50LDO_ADDR, block, ETHEREUM, web3=node)
    # [token, balance, staked, locked]
    assert ldo == [ETHTokenAddr.LDO, 576.5066246253847, 0, 0]
    assert wsteth == [ETHTokenAddr.wstETH, 0.5871242486850999, 0, 0]

    usdt, usdc, dai = Balancer.underlying(WALLET_N6, bbaUSD_ADDR, block, ETHEREUM, web3=node, reward=True)
    # [token, balance, staked, locked]
    assert usdt == [ETHTokenAddr.USDT, 34481.50498155418, 0, 0]
    assert usdc == [ETHTokenAddr.USDC, 40407.38426818376, 0, 0]
    assert dai == [ETHTokenAddr.USDC, 39386.25356751313, 0, 0]

    usdt, usdc, dai = Balancer.underlying(WALLET_39d, bbaUSD_ADDR, block, ETHEREUM, web3=node, reward=True)
    # [token, balance, staked, locked]
    assert usdt == [ETHTokenAddr.USDT, 8507.3242092116, 0, 0]
    assert usdc == [ETHTokenAddr.USDC, 9969.365275660934, 0, 0]
    assert dai == [ETHTokenAddr.USDC, 9717.430508450754, 0, 0]
   

def test_pool_balances():
    block = 16978206
    node = get_node(ETHEREUM, block)

    usdc, weth = Balancer.pool_balances(B50USDC50WETH_ADDR, block, ETHEREUM, web3=node)
    assert usdc == [ETHTokenAddr.USDC, 1129072.214823]
    assert weth == [ETHTokenAddr.WETH, 601.5359543423447]

def test_pool_balances2():
    block = 17117344
    node = get_node(ETHEREUM, block)

    usdt, usdc, dai = Balancer.pool_balances(bbaUSD_ADDR, block, ETHEREUM, web3=node)
    assert usdt == [ETHTokenAddr.USDT, 11390997.351595458]
    assert usdc == [ETHTokenAddr.USDC, 13348617.104445048]
    assert dai == [ETHTokenAddr.DAI, 13011285.624476457]

    usdt = Balancer.pool_balances(bbaUSDT_ADDR, block, ETHEREUM, web3=node)
    assert usdt == [ETHTokenAddr.USDT, 11391113.139048]

    usdc = Balancer.pool_balances(bbaUSDC_ADDR, block, ETHEREUM, web3=node)
    assert usdc == [ETHTokenAddr.USDC, 13348911.876651]

    dai = Balancer.pool_balances(bbaDAI_ADDR, block, ETHEREUM, web3=node)
    assert dai == [ETHTokenAddr.DAI, 13011503.946034884]

def test_unwrap():
    block = 16950590
    node = get_node(ETHEREUM, block)

    lptoken_amount = 1
    usdt, usdc, dai = Balancer.unwrap(lptoken_amount, bbaUSD_ADDR, block, ETHEREUM, web3=node)
    assert usdt == [ETHTokenAddr.USDT, 0.2544853984016551]
    assert usdc == [ETHTokenAddr.USDC, 0.36952776509915247]
    assert dai == [ETHTokenAddr.DAI, 0.3804754985865416]

    lptoken_amount = 0.010622337758482546
    dai, weth = Balancer.unwrap(lptoken_amount, B60WETH40DAI_ADDR, block, ETHEREUM, web3=node)
    assert dai == [ETHTokenAddr.DAI, 0.3998802387901373]
    assert weth == [ETHTokenAddr.WETH, 0.0003284487726480976]


def test_swap_fees():
    blockstart = date_to_block('2023-02-20 18:25:00', ETHEREUM)
    blockend = date_to_block('2023-02-20 18:30:00', ETHEREUM)
    swaps = Balancer.swap_fees(B80BAL20WETH_ADDR, blockstart, blockend, ETHEREUM)

    assert swaps['swaps'] == [{'block': 16671528, 'tokenIn': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amountIn': 0.09017533361647305},
                              {'block': 16671542, 'tokenIn': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'amountIn': 0.07953507489302288}]


def test_swap_fees_apr():
    blockend = date_to_block('2023-02-20 18:30:00', ETHEREUM)
    swaps_apr = Balancer.get_swap_fees_APR(B80BAL20WETH_ADDR, ETHEREUM, blockend)
    assert swaps_apr == 0.5961250860104128

test_underlying2()
test_pool_balances2()