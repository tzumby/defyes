from decimal import Decimal

from defi_protocols import Balancer
from defi_protocols.constants import ETHEREUM, XDAI, ETHTokenAddr, GnosisTokenAddr
from defi_protocols.functions import date_to_block

WALLET_N1 = "0x31cD267D34EC6368eac930Be4f412dfAcc71A844"
WALLET_N2 = "0x4b0429F3db75dbA6B82c32a200C9C298ffC05839"
WALLET_N3 = "0xe8fAF95AD24A467ddDc4e100a68398B31D3dCdd6"
WALLET_N4 = "0x64aE36eeaC5BF9c1F4b7Cc6F0Fa32bBa19aaF9Bc"
WALLET_N5 = "0xce88686553686DA562CE7Cea497CE749DA109f9F"
WALLET_N6 = "0x43b650399F2E4D6f03503f44042fabA8F7D73470"
WALLET_39d = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
B60WETH40DAI_ADDR = "0x0b09deA16768f0799065C475bE02919503cB2a35"
B50USDC50WETH_ADDR = "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8"
B80BAL20WETH_ADDR = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"
BstETHSTABLE_ADDR = "0x32296969Ef14EB0c6d29669C550D4a0449130230"
B50wstETH50LDO_ADDR = "0x5f1f4e50ba51d723f12385a8a9606afc3a0555f5"
bbaUSD_ADDR = "0xA13a9247ea42D743238089903570127DdA72fE44"
bbaUSDT_ADDR = "0x2f4eb100552ef93840d5adc30560e5513dfffacb"
bbaUSDC_ADDR = "0x82698aecc9e28e9bb27608bd52cf57f704bd1b83"
bbaDAI_ADDR = "0xae37d54ae477268b9997d4161b96b8200755935c"

# Gnosis Chain
WALLET_e6f = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"
bb_ag_USD_ADDR = "0xfedb19ec000d38d92af4b21436870f115db22725"
B50bbagGNO50bbagUSD_ADDR = "0xB973Ca96a3f0D61045f53255E319AEDb6ED49240"
bb_ag_WXDAI_ADDR = "0x41211bba6d37f5a74b22e667533f080c7c7f3f13"
bb_ag_GNO_ADDR = "0xffff76a3280e95dc855696111c2562da09db2ac0"


def test_liquidity_pool():
    block = 16950590

    lp = Balancer.LiquidityPool(ETHEREUM, block, B60WETH40DAI_ADDR)
    assert (
        lp.poolid
        == b"\x0b\t\xde\xa1gh\xf0y\x90e\xc4u\xbe\x02\x91\x95\x03\xcb*5\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a"
    )
    assert lp.decimals == 18
    assert lp.supply == 12835022143788475405205
    assert lp.bpt_index is None
    assert lp.scaling_factors is None

    lp = Balancer.LiquidityPool(ETHEREUM, block, bbaUSD_ADDR)
    assert (
        lp.poolid == b"\xa1:\x92G\xeaB\xd7C#\x80\x89\x905p\x12}\xdar\xfeD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03]"
    )
    assert lp.decimals == 18
    assert lp.supply == 45626173875220118192194148
    assert lp.bpt_index == 2
    assert lp.scaling_factors == [
        1008896757769783573,
        1003250365192438010,
        1000000000000000000,
        1002548558018035032,
    ]


def test_gauge_address():
    block = 16978206
    assert (
        Balancer.GaugeFactory(ETHEREUM, block, B60WETH40DAI_ADDR).gauge_address
        == "0x4ca6AC0509E6381Ca7CD872a6cdC0Fbf00600Fa1"
    )
    assert (
        Balancer.GaugeFactory(ETHEREUM, block, BstETHSTABLE_ADDR).gauge_address
        == "0xcD4722B7c24C29e0413BDCd9e51404B4539D14aE"
    )

    block = 27628264
    assert (
        Balancer.GaugeFactory(XDAI, block, B50bbagGNO50bbagUSD_ADDR).gauge_address
        == "0x7E13b8b95d887c2326C25e71815F33Ea10A2674e"
    )


def test_pool_balances():
    block = 16978206
    balances = Balancer.pool_balances(ETHEREUM, B50USDC50WETH_ADDR, block)
    assert balances == {
        ETHTokenAddr.USDC: Decimal("1129072.214823"),
        ETHTokenAddr.WETH: Decimal("601.535954342344676691"),
    }

    block = 17117344
    balances = Balancer.pool_balances(ETHEREUM, bbaUSD_ADDR, block)
    assert balances == {
        ETHTokenAddr.USDT: Decimal("11433582.31554748359005298347"),
        ETHTokenAddr.USDC: Decimal("13368829.78950840748853951224"),
        ETHTokenAddr.DAI: Decimal("13416454.19566038579649334747"),
    }

    usdt = Balancer.pool_balances(ETHEREUM, bbaUSDT_ADDR, block)
    assert usdt[ETHTokenAddr.USDT] == Decimal("11433698.53586857519047922515")

    usdc = Balancer.pool_balances(ETHEREUM, bbaUSDC_ADDR, block)
    assert usdc[ETHTokenAddr.USDC] == Decimal("13369125.00806304894840304454")

    dai = Balancer.pool_balances(ETHEREUM, bbaDAI_ADDR, block)
    assert dai[ETHTokenAddr.DAI] == Decimal("13416679.31570410197485793129")

    block = 27628264
    balances = Balancer.pool_balances(XDAI, bb_ag_WXDAI_ADDR, block)
    assert balances[GnosisTokenAddr.WXDAI] == Decimal("1295439.981731337648045247778")

    balances = Balancer.pool_balances(XDAI, B50bbagGNO50bbagUSD_ADDR, block)
    assert balances == {
        GnosisTokenAddr.WXDAI: Decimal("327217.3285011014510966714956"),
        GnosisTokenAddr.USDT: Decimal("182785.2866365983481610436107"),
        GnosisTokenAddr.USDC: Decimal("304180.9070344813788008988656"),
        GnosisTokenAddr.GNO: Decimal("7700.623246950826914818782253"),
    }

    gno = Balancer.pool_balances(XDAI, bb_ag_GNO_ADDR, block)
    assert gno[GnosisTokenAddr.GNO] == Decimal("26159.71190211541086527825594")


def test_unwrap():
    block = 16950590
    lptoken_amount = 1
    unwrap = Balancer.unwrap(ETHEREUM, bbaUSD_ADDR, lptoken_amount, block)
    assert unwrap == {
        ETHTokenAddr.USDT: Decimal("0.2544855265987162735881749720"),
        ETHTokenAddr.USDC: Decimal("0.3695278389467781030866438160"),
        ETHTokenAddr.DAI: Decimal("0.3804761470992138348159360416"),
    }

    lptoken_amount = Decimal("0.0106223377584825466601881061023959773592650890350341796875")
    unwrap = Balancer.unwrap(ETHEREUM, B60WETH40DAI_ADDR, lptoken_amount, block)
    assert unwrap == {
        ETHTokenAddr.DAI: Decimal("0.3998802387901373103114663897"),
        ETHTokenAddr.WETH: Decimal("0.0003284487726480976462916290608"),
    }

    block = 27628264
    lptoken_amount = 1000
    unwrap = Balancer.unwrap(XDAI, B50bbagGNO50bbagUSD_ADDR, lptoken_amount, block)
    assert unwrap == {
        GnosisTokenAddr.WXDAI: Decimal("2072.099936394024014750631244"),
        GnosisTokenAddr.USDT: Decimal("1157.485706971609760143788076"),
        GnosisTokenAddr.USDC: Decimal("1926.222064722662625127836312"),
        GnosisTokenAddr.GNO: Decimal("48.76410736953816262713084976"),
    }


def test_gauge_rewards():
    block = 16978206

    gauge_address = Balancer.GaugeFactory(ETHEREUM, block, B60WETH40DAI_ADDR).gauge_address
    gauge = Balancer.Gauge(ETHEREUM, block, gauge_address)
    bal_rewards = gauge.get_bal_rewards(WALLET_N1)
    assert bal_rewards == {ETHTokenAddr.BAL: Decimal("0.000001267800098374")}

    gauge_address = Balancer.GaugeFactory(ETHEREUM, block, BstETHSTABLE_ADDR).gauge_address
    gauge = Balancer.Gauge(ETHEREUM, block, gauge_address)
    rewards = gauge.get_rewards(WALLET_N3)
    assert rewards == {ETHTokenAddr.LDO: 0}


def test_vebal_rewards():
    block = 16950590

    vebal_distributor = Balancer.VebalFeeDistributor(ETHEREUM, block)
    vebal_rewards = vebal_distributor.get_rewards(WALLET_N2)

    assert vebal_rewards == {
        ETHTokenAddr.BAL: Decimal("0.000019372013715193"),
        ETHTokenAddr.BB_A_USD_OLD: Decimal("0"),
        ETHTokenAddr.BB_A_USD: Decimal("0.000210261212072964"),
    }


def test_underlying():
    block = 16978206
    underlying = Balancer.underlying(ETHEREUM, WALLET_N1, B60WETH40DAI_ADDR, block, reward=True)
    assert {
        "block": 16978206,
        "blockchain": "ethereum",
        "positions": {
            "0x0b09deA16768f0799065C475bE02919503cB2a35": [
                {
                    "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                    "balance": Decimal("0E-17"),
                    "state": "balance",
                },
                {
                    "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                    "balance": Decimal("0.4064524767585684232500351728"),
                    "state": "staked",
                },
                {
                    "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                    "balance": Decimal("0E-17"),
                    "state": "locked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0E-18"),
                    "state": "balance",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0.0003249882874596042694139236462"),
                    "state": "staked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0E-18"),
                    "state": "locked",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0.000001267800098374"),
                    "state": "bal_reward",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2",
                    "balance": Decimal("0"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                    "balance": Decimal("0"),
                    "state": "vebal_reward",
                },
            ]
        },
        "positions_key": "liquidity_pool_address",
        "protocol": "Balancer",
        "underlying_version": 0,
    } == underlying

    underlying = Balancer.underlying(ETHEREUM, WALLET_N2, [B50USDC50WETH_ADDR, B80BAL20WETH_ADDR], block, reward=True)
    assert {
        "block": 16978206,
        "blockchain": "ethereum",
        "positions": {
            "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56": [
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0E-18"),
                    "state": "balance",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("1.381597279600636357432913945"),
                    "state": "staked",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("1.000114468622601307282666145"),
                    "state": "locked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0E-18"),
                    "state": "balance",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0.001299296197959105460435983484"),
                    "state": "staked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0.0009405381335007070147710888177"),
                    "state": "locked",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0.000019372013715193"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2",
                    "balance": Decimal("0"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                    "balance": Decimal("0.000210261212072964"),
                    "state": "vebal_reward",
                },
            ],
            "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8": [
                {
                    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                    "balance": Decimal("10.24608281454370054240898545"),
                    "state": "balance",
                },
                {
                    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                    "balance": Decimal("10.58962966563745330384918783"),
                    "state": "staked",
                },
                {
                    "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                    "balance": Decimal("0.000000"),
                    "state": "locked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0.005458806906415149638057440356"),
                    "state": "balance",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0.005641838408050662404836892297"),
                    "state": "staked",
                },
                {
                    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                    "balance": Decimal("0E-18"),
                    "state": "locked",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0.002255938639324377"),
                    "state": "bal_reward",
                },
                {
                    "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                    "balance": Decimal("0.000019372013715193"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0x7B50775383d3D6f0215A8F290f2C9e2eEBBEceb2",
                    "balance": Decimal("0"),
                    "state": "vebal_reward",
                },
                {
                    "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                    "balance": Decimal("0.000210261212072964"),
                    "state": "vebal_reward",
                },
            ],
        },
        "positions_key": "liquidity_pool_address",
        "protocol": "Balancer",
        "underlying_version": 0,
    } == underlying


# def test_underlying2():
#    block = 17117344
#    node = get_node(ETHEREUM, block)
#
#    steth, weth = Balancer.underlying(WALLET_N4, BstETHSTABLE_ADDR, block, ETHEREUM, web3=node)
#    # [token, balance, staked, locked]
#    assert steth == [ETHTokenAddr.stETH, Decimal('11.37232115107245169857021374'), Decimal('0'), Decimal('0')]
#    assert weth == [ETHTokenAddr.WETH, Decimal('10.93914528430790259522572181'), Decimal('0'), Decimal('0')]
#
#    ldo, wsteth = Balancer.underlying(WALLET_N5, B50wstETH50LDO_ADDR, block, ETHEREUM, web3=node)
#    # [token, balance, staked, locked]
#    assert ldo == [ETHTokenAddr.LDO, Decimal('576.5066246253847582651532174'), Decimal('0'), Decimal('0')]
#    assert wsteth == [ETHTokenAddr.wstETH, Decimal('0.5871242486850998522269758922'), Decimal('0'), Decimal('0')]
#
#    usdt, usdc, dai = Balancer.underlying(WALLET_N6, bbaUSD_ADDR, block, ETHEREUM, web3=node)
#    # [token, balance, staked, locked]
#    assert usdt == [ETHTokenAddr.USDT, Decimal('34610.41324141304294002886857'), Decimal('0'), Decimal('0')]
#
#    assert usdc == [ETHTokenAddr.USDC, Decimal('40468.56976223580477414327278'), Decimal('0'), Decimal('0')]
#    assert dai == [ETHTokenAddr.DAI, Decimal('40612.73283657301313797645226'), Decimal('0'), Decimal('0')]
#
#    usdt, usdc, dai = Balancer.underlying(WALLET_39d, bbaUSD_ADDR, block, ETHEREUM, web3=node)
#    # [token, balance, staked, locked]
#    assert usdt == [ETHTokenAddr.USDT, Decimal('8539.128631914474969130263864'), Decimal('0'), Decimal('0')]
#    assert usdc == [ETHTokenAddr.USDC, Decimal('9984.461044684933239332062933'), Decimal('0'), Decimal('0')]
#    assert dai == [ETHTokenAddr.DAI, Decimal('10020.02915614176748146463595'), Decimal('0'), Decimal('0')]
#
#
# def test_underlying3():
#    block = 28275634
#    node = get_node(XDAI, block)
#
#    [[wxdai, usdt, usdc], [bal_rewards]] = Balancer.underlying(WALLET_e6f, bb_ag_USD_ADDR, block, XDAI, web3=node, reward=True)
#    # [token, balance, staked, locked]
#    assert wxdai == [GnosisTokenAddr.WXDAI, Decimal('0'), Decimal('225689.5790202310752030943317'), Decimal('0')]
#    assert usdt == [GnosisTokenAddr.USDT, Decimal('0'), Decimal('157457.9259177606355118786078'), Decimal('0')]
#    assert usdc == [GnosisTokenAddr.USDC, Decimal('0'), Decimal('193285.0087113081451905116408'), Decimal('0')]
#    assert bal_rewards == [GnosisTokenAddr.BAL, Decimal('72.028749058272541921')]
#
#    [[wxdai, usdt, usdc, gno], [bal_rewards]] = Balancer.underlying(WALLET_e6f, B50bbagGNO50bbagUSD_ADDR, block, XDAI, web3=node, reward=True)
#    # [token, balance, staked, locked]
#    assert wxdai == [GnosisTokenAddr.WXDAI, Decimal('0'), Decimal('333762.1862551265554595821346'), Decimal('0')]
#    assert usdt == [GnosisTokenAddr.USDT, Decimal('0'), Decimal('232857.4576888133034458734522'), Decimal('0')]
#    assert usdc == [GnosisTokenAddr.USDC, Decimal('0'), Decimal('285840.5220032092259613956715'), Decimal('0')]
#    assert gno == [GnosisTokenAddr.GNO, Decimal('0'), Decimal('7325.982201639479819930022796'), Decimal('0')]
#    assert bal_rewards == [GnosisTokenAddr.BAL, Decimal('422.039676607937704001')]
#
#
def test_swap_fees():
    blockstart = date_to_block("2023-02-20 18:25:00", ETHEREUM)
    blockend = date_to_block("2023-02-20 18:30:00", ETHEREUM)

    vault_address = Balancer.Vault(ETHEREUM, blockend).address
    lp = Balancer.LiquidityPool(ETHEREUM, blockend, B80BAL20WETH_ADDR)
    swaps = lp.swap_fees(vault_address, blockstart)
    assert swaps == [
        {
            "block": 16671528,
            "token_in": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "amount_in": Decimal("0.09017533361647305728"),
        },
        {
            "block": 16671542,
            "token_in": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "amount_in": Decimal("0.0795350748930228736"),
        },
    ]


def test_swap_fees_apr():
    blockend = date_to_block("2023-02-20 18:30:00", ETHEREUM)
    apr = Balancer.get_swap_fees_apr(B80BAL20WETH_ADDR, ETHEREUM, blockend)
    assert apr == Decimal("0.596125086010151913782740200")
    apy = Balancer.get_swap_fees_apr(B80BAL20WETH_ADDR, ETHEREUM, blockend, apy=True)
    assert apy == Decimal("0.815071898400229530363657020")
