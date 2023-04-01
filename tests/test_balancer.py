from defi_protocols import Balancer
from defi_protocols.constants import ETHEREUM, POLYGON, BAL_POL, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_contract, get_node

WALLET_N1 = '0x31cD267D34EC6368eac930Be4f412dfAcc71A844'
WALLET_N2 = '0x4b0429F3db75dbA6B82c32a200C9C298ffC05839'
B60WETH40DAI_ADDR = '0x0b09deA16768f0799065C475bE02919503cB2a35'
B50USDC50WETH_ADDR = '0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8'


def test_get_gauge_factory_address():
    gauge_address = Balancer.get_gauge_factory_address(ETHEREUM)
    assert Balancer.LIQUIDITY_GAUGE_FACTORY_ETHEREUM == gauge_address


def test_get_bal_address():
    assert ETHTokenAddr.BAL == Balancer.get_bal_address(ETHEREUM)
    assert BAL_POL == Balancer.get_bal_address(POLYGON)


def test_get_lptoken_data():
    block = 16950590
    lptoken_data = Balancer.get_lptoken_data(B60WETH40DAI_ADDR, block, ETHEREUM)

    assert list(lptoken_data.keys()) == ['contract', 'poolId', 'decimals', 'totalSupply', 'isBoosted', 'bptIndex']
    assert lptoken_data['poolId'] == b'\x0b\t\xde\xa1gh\xf0y\x90e\xc4u\xbe\x02\x91\x95\x03\xcb*5\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a'
    assert lptoken_data['decimals'] == 18
    assert lptoken_data['totalSupply'] == 12835022143788475405205
    assert not lptoken_data['isBoosted']
    assert lptoken_data['bptIndex'] is None


def test_bal_rewards():
    block = 16950590
    node = get_node(ETHEREUM, block)

    gauge_factory_address = Balancer.get_gauge_factory_address(ETHEREUM)
    gauge_factory_contract = get_contract(gauge_factory_address,
                                          ETHEREUM,
                                          web3=node,
                                          abi=Balancer.ABI_LIQUIDITY_GAUGE_FACTORY,
                                          block=block)
    gauge_address = gauge_factory_contract.functions.getPoolGauge(B50USDC50WETH_ADDR).call()
    gauge_contract = get_contract(gauge_address,
                                  ETHEREUM,
                                  web3=node,
                                  abi=Balancer.ABI_GAUGE,
                                  block=block)

    bal_rewards = Balancer.get_bal_rewards(node, gauge_contract, WALLET_N2, block, ETHEREUM)
    assert bal_rewards[0] == ETHTokenAddr.BAL
    assert bal_rewards[1] == 0.002223198404020921
