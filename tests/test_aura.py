from tempfile import NamedTemporaryFile
from defi_protocols import Aura
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node, get_contract


B50OHM50wstETH_ADDR = "0xd4f79CA0Ac83192693bce4699d0c10C66Aa6Cf0F"
auraOHMwstETH_TOKEN = "0x0EF97ef0e20F84e82ec2D79CBD9Eda923C3DAF09"
OHMwstETHgauge_ADDR = "0xE879f17910E77c01952b97E4A098B0ED15B6295c"
auraOHMwstETHvault_ADDR = "0x636024F9Ddef77e625161b2cCF3A2adfbfAd3615"  # Aura base reward pool
auraOHMwstETHstash_ADDR = "0x04B4e364FFBF1C8f938D6A6258bDC8cb503DEB64"  # Aura extra reward pool stash

WALLET_N1 = "0xb74e5e06f50fa9e4eF645eFDAD9d996D33cc2d9D"


def test_db_uptodate():
    with NamedTemporaryFile() as tmpfile:
        uptodate = Aura.update_db(tmpfile.name)
        assert uptodate is False, "DB is outdated"


def test_get_pool_info():
    block = 17012817
    node = get_node(ETHEREUM, block)
    booster_contract = get_contract(Aura.BOOSTER, ETHEREUM, web3=node, abi=Aura.ABI_BOOSTER, block=block)
    pool_info = Aura.get_pool_info(booster_contract, B50OHM50wstETH_ADDR, block)

    assert pool_info == [B50OHM50wstETH_ADDR,
                         auraOHMwstETH_TOKEN,
                         OHMwstETHgauge_ADDR,
                         auraOHMwstETHvault_ADDR,
                         auraOHMwstETHstash_ADDR,
                         False]


def test_get_rewards():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(auraOHMwstETHvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    rewards = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, ETHEREUM)
    assert rewards == [ETHTokenAddr.BAL, 1.8716673573728932]
