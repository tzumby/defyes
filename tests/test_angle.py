from decimal import Decimal

from defi_protocols import Angle
from defi_protocols.constants import ETHEREUM

agEUR = "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8"

def test_angle_treasury():
    wallet = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
    block = 17451062

    t = Angle.Treasury(ETHEREUM)
    assert t.stable_coin == agEUR
    assert ['0x241D7598BD1eb819c0E9dEd456AcB24acA623679',
            '0x1beCE8193f8Dc2b170135Da9F1fA8b81C7aD18b1',
            '0x73aaf8694BA137a7537E7EF544fcf5E2475f227B',
            '0x8E2277929B2D849c0c344043D9B9507982e6aDd0',
            '0xdEeE8e8a89338241fe622509414Ff535fB02B479',
            '0x0652B4b3D205300f9848f0431296D67cA4397f3b',
            '0xE1C084e6E2eC9D32ec098e102a73C4C27Eb9Ee58',
            '0x0B3AF9fb0DE42AE70432ABc5aaEaB8F9774bf87b',
            '0x989ed2DDCD4D2DC237CE014432aEb40EfE738E31',
            '0x29e9D3D8e295E23B1B39DCD3D8D595761E032306',
            '0xe0C8B6c4ea301C8A221E8838ca5B80Ac76E7A10b',
            '0x913E8e1eD659C27613E937a6B6119b91D985094c',
            '0x96de5c30F2BF4683c7903F3e921F720602F8868A'] == t.get_all_vault_managers_addrs(block)

    # everything below is WIP
    Angle.underlying(ETHEREUM, wallet, block)
