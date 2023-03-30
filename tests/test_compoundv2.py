from defi_protocols import Compound
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node

CTOKEN_CONTRACTS = {
    'cbat_contract': '0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E',
    'cdai_contract': '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643',
    'ceth_contract': '0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5',
    'crep_contract': '0x158079Ee67Fce2f58472A96584A73C7Ab9AC95c1',
    'cusdc_contract': '0x39AA39c021dfbaE8faC545936693aC917d5E7563',
    'cusdt_contract': '0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9',
    'cwbtc_contract': '0xC11b1268C1A384e55C48c2391d8d480264A3A7F4',
    'czrx_contract': '0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407',
    'csai_contract': '0xF5DCe57282A584D2746FaF1593d3121Fcac444dC',
    'cuni_contract': '0x35A18000230DA775CAc24873d00Ff85BccdeD550',
    'ccomp_contract': '0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4',
    'cwbtc2_contract': '0xccF4429DB6322D5C611ee964527D42E5d685DD6a',
    'ctusd_contract': '0x12392F67bdf24faE0AF363c24aC620a2f67DAd86',
    'clink_contract': '0xFAce851a4921ce59e912d19329929CE6da6EB0c7',
    'cmkr_contract': '0x95b4eF2869eBD94BEb4eEE400a99824BF5DC325b',
    'csushi_contract': '0x4B0181102A0112A2ef11AbEE5563bb4a3176c9d7',
    'caave_contract': '0xe65cdB6479BaC1e22340E4E755fAE7E509EcD06c',
    'cyfi_contract': '0x80a2AE356fc9ef4305676f7a3E2Ed04e12C33946',
    'cusdp_contract': '0x041171993284df560249B57358F931D9eB7b925D',
    'cfei_contract': '0x7713DD9Ca933848F6819F38B8352D9A15EA73F67'
    }

WALLET_N1 = '0x31cD267D34EC6368eac930Be4f412dfAcc71A844'
WALLET_N2 = '0x99e881e9e89152b0add27c367f0761f0fbe5ddc3'


def test_get_comptoller_address():
    comptroller_address = Compound.get_comptoller_address(ETHEREUM)
    assert Compound.COMPTROLLER_ETHEREUM == comptroller_address


def test_get_compound_lens_address():
    comp_lens_address = Compound.get_compound_lens_address(ETHEREUM)
    assert Compound.COMPOUND_LENS_ETHEREUM == comp_lens_address


def test_get_compound_token_address():
    comp_eth = Compound.get_compound_token_address(ETHEREUM)
    assert ETHTokenAddr.COMP == comp_eth


def test_get_ctokens_contract_list():
    block = 16904422
    web3 = get_node(ETHEREUM, block)
    ctokens_list = Compound.get_ctokens_contract_list(ETHEREUM, web3, block)
    assert ctokens_list == list(CTOKEN_CONTRACTS.values())


def test_get_ctoken_data():
    block = 16904422
    wallet1_cdai = Compound.get_ctoken_data(CTOKEN_CONTRACTS['cdai_contract'], WALLET_N1, block, ETHEREUM)
    assert wallet1_cdai['underlying'] == ETHTokenAddr.DAI
    assert wallet1_cdai['decimals'] == 8
    assert wallet1_cdai['borrowBalanceStored'] == 0
    assert wallet1_cdai['balanceOf'] == 4505674362
    assert wallet1_cdai['exchangeRateStored'] == 221942359677997719508746620

    block = 16906410
    wallet1_ceth = Compound.get_ctoken_data(CTOKEN_CONTRACTS['ceth_contract'], WALLET_N1, block, ETHEREUM)
    assert wallet1_ceth['underlying'] == ZERO_ADDRESS
    assert wallet1_ceth['decimals'] == 8
    assert wallet1_ceth['borrowBalanceStored'] == 0
    assert wallet1_ceth['balanceOf'] == 4979680
    assert wallet1_ceth['exchangeRateStored'] == 200816109095853438085339051

    block = 16906410
    wallet2_ccomp = Compound.get_ctoken_data(CTOKEN_CONTRACTS['ccomp_contract'], WALLET_N2, block, ETHEREUM)
    assert wallet2_ccomp['underlying'] == ETHTokenAddr.COMP
    assert wallet2_ccomp['decimals'] == 8
    assert wallet2_ccomp['borrowBalanceStored'] == 0
    assert wallet2_ccomp['balanceOf'] == 24296781813013
    assert wallet2_ccomp['exchangeRateStored'] == 204174793505775477876721754


def test_underlying():
    block = 16904422
    dai_underlying = Compound.underlying(WALLET_N1, ETHTokenAddr.DAI, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert dai_underlying == [['0x6B175474E89094C44Da98b954EedeAC495271d0F', 0.9999999998429369]]

    block = 16906410
    eth_underlying = Compound.underlying(WALLET_N1, ZERO_ADDRESS, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert eth_underlying == [['0x0000000000000000000000000000000000000000', 0.0009999999621424396]]


def test_underlying_all():
    block = 16906410
    underlyings = Compound.underlying_all(WALLET_N1, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert underlyings == [[ETHTokenAddr.DAI, 1.0000108840576543],
                           [ZERO_ADDRESS, 0.0009999999621424396]]


def test_all_comp_rewards():
    block = 16924820
    rewards = Compound.all_comp_rewards(WALLET_N1, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert rewards[0][0] == ETHTokenAddr.COMP
    assert rewards[0][1] == 1.508535739321e-06


def test_unwrap():
    block = 16924820
    wallet1_cdai = Compound.get_ctoken_data(CTOKEN_CONTRACTS['cdai_contract'],
                                            WALLET_N1,
                                            block,
                                            ETHEREUM,
                                            web3=get_node(ETHEREUM))
    ctoken_amount = wallet1_cdai['balanceOf']
    ctoken_address = CTOKEN_CONTRACTS['cdai_contract']
    unwrapped_data = Compound.unwrap(ctoken_amount, ctoken_address, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert unwrapped_data == [ETHTokenAddr.DAI, 100012432.30888236]


def test_get_apr():
    block = 16924820
    comp_apr = Compound.get_apr(ETHTokenAddr.COMP, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert comp_apr == [{'metric': 'apr', 'type': 'supply', 'value': 0.0028302645027622475},
                        {'metric': 'apr', 'type': 'borrow', 'value': 0.05500756675758112}]

    dai_apy = Compound.get_apr(ETHTokenAddr.DAI, block, ETHEREUM, web3=get_node(ETHEREUM), apy=True)
    assert dai_apy == [{'metric': 'apy', 'type': 'supply', 'value': 0.017116487300299577},
                       {'metric': 'apy', 'type': 'borrow', 'value': 0.03595587221146879}]

    dai_apr_with_contract = Compound.get_apr(ETHTokenAddr.DAI,
                                             block,
                                             ETHEREUM,
                                             web3=get_node(ETHEREUM),
                                             ctoken_address=CTOKEN_CONTRACTS['cdai_contract'])
    assert dai_apr_with_contract == [{'metric': 'apr', 'type': 'supply', 'value': 0.016971650612873646},
                                     {'metric': 'apr', 'type': 'borrow', 'value': 0.03532454536880891}]


def test_get_comp_apr():
    block = 16924820
    usdc_comp_apr = Compound.get_comp_apr(ETHTokenAddr.USDC, block, ETHEREUM, web3=get_node(ETHEREUM))
    assert usdc_comp_apr == [{'metric': 'apr', 'type': 'supply', 'value': 0.0},
                             {'metric': 'apr', 'type': 'borrow', 'value': 0.004109315639766464}]

    dai_comp_apy = Compound.get_comp_apr(ETHTokenAddr.DAI, block, ETHEREUM, web3=get_node(ETHEREUM), apy=True)
    assert dai_comp_apy == [{'metric': 'apy', 'type': 'supply', 'value': 0.007943711809621057},
                            {'metric': 'apy', 'type': 'borrow', 'value': 0.01409698572150675}]

    sushi_apr_contract = Compound.get_apr(ETHTokenAddr.SUSHI,
                                          block,
                                          ETHEREUM,
                                          web3=get_node(ETHEREUM),
                                          ctoken_address=CTOKEN_CONTRACTS['csushi_contract'])
    assert sushi_apr_contract == [{'metric': 'apr', 'type': 'supply', 'value': 0.003473483836557989},
                                  {'metric': 'apr', 'type': 'borrow', 'value': 0.05069088908626895}]
