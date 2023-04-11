from tempfile import NamedTemporaryFile
from defi_protocols import Aura
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node, get_contract


balancer_50OHM50wstETH_ADDR = "0xd4f79CA0Ac83192693bce4699d0c10C66Aa6Cf0F"
aura_OHMwstETH_TOKEN = "0x0EF97ef0e20F84e82ec2D79CBD9Eda923C3DAF09"
balancer_OHMwstETHgauge_ADDR = "0xE879f17910E77c01952b97E4A098B0ED15B6295c"
aura_OHMwstETHvault_ADDR = "0x636024F9Ddef77e625161b2cCF3A2adfbfAd3615"  # Aura base reward pool
aura_OHMwstETHstash_ADDR = "0x04B4e364FFBF1C8f938D6A6258bDC8cb503DEB64"  # Aura extra reward pool stash

balancer_80SD20WETH_ADDR = "0xE4010EF5E37dc23154680f23c4A0d48BFca91687"
aura_80SD20WETH_TOKEN = "0xfBc4BA0dd708850D9Aa809090873F71E188798EB"
balancer_80SD20WETHgauge_ADDR = "0x37eCa8DaaB052E722e3bf8ca861aa4e1C047143b"
aura_80SD20WETHvault_ADDR = "0x890bdF60C6566Df09Ce37132DEb652050E5685bD"  # Aura base reward pool
aura_80SD20WETHstash_ADDR = "0x740f9Af398CB77C7cD67EA9744d0F02D8F23de70"  # Aura extra reward pool stash

balancer_auraBALSTABLE_ADDR = "0x3dd0843A028C86e0b760b1A76929d1C5Ef93a2dd"
aura_auraBALSTABLE_TOKEN = "0x12e9DA849f12d47707A94e29f781f1cd20A7f49A"
balancer_auraBALSTABLEgauge_ADDR = "0x0312AA8D0BA4a1969Fddb382235870bF55f7f242"
aura_auraBALSTABLEvault_ADDR = "0xACAdA51C320947E7ed1a0D0F6b939b0FF465E4c2"
aura_auraBALSTABLEstash_ADDR = "0x7b3307af981F55C8D6cd22350b08C39Ec7Ec481B"

WALLET_N1 = "0xb74e5e06f50fa9e4eF645eFDAD9d996D33cc2d9D"
WALLET_N2 = "0xA2f32ADc4908565113cba479821f435d453968Be"
WALLET_N3 = "0x6d707F73f621722fEc0E6A260F43f24cCC8d4997"


def test_db_uptodate():
    with NamedTemporaryFile() as tmpfile:
        uptodate = Aura.update_db(tmpfile.name)
        assert uptodate is False, "DB is outdated"


def test_get_pool_info():
    block = 17012817
    node = get_node(ETHEREUM, block)
    booster_contract = get_contract(Aura.BOOSTER, ETHEREUM, web3=node, abi=Aura.ABI_BOOSTER, block=block)
    pool_info = Aura.get_pool_info(booster_contract, balancer_50OHM50wstETH_ADDR, block)

    assert pool_info == [balancer_50OHM50wstETH_ADDR,
                         aura_OHMwstETH_TOKEN,
                         balancer_OHMwstETHgauge_ADDR,
                         aura_OHMwstETHvault_ADDR,
                         aura_OHMwstETHstash_ADDR,
                         False]


def test_get_rewards():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(aura_OHMwstETHvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    rewards = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, ETHEREUM)
    assert rewards == [ETHTokenAddr.BAL, 1.8716673573728932]


def test_get_extra_rewards():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(aura_auraBALSTABLEvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    rewards = Aura.get_extra_rewards(node, rewarder_contract, WALLET_N3, block, ETHEREUM)
    assert rewards[0] == [ETHTokenAddr.AURA, 0.198621417050926]
