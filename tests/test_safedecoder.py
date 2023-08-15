from defyes.constants import Chain
from defyes.SafeDecoder import get_safe_functions


def test_safe_functions():
    block = (17117344,)
    # tx1 = '0x2971c45416cbf234fe8939599dbb64d5c53210e76e4ff32d89188fa9bea30f87' # multisend
    # tx2 = '0x3c0fbad1350d84a159acef5c3e6fe350e10d44dc894bb3ee6f784b0c167e791f' # exec with role
    tx3 = "0xd6ef0254c88760e5a2e58924bbaa28f8700341bfa91df469fc9c6f904b732e34"  # single call
    test = get_safe_functions(tx3, block, Chain.ETHEREUM)
    assert test["operation"] == 0
    assert test["to_address"] == "0xC128a9954e6c874eA3d62ce62B468bA073093F25"
    assert test["value"] == 0
    assert test["data_output"][0].fn_name == "increase_amount"
    assert test["data_output"][1]["_value"] == 15306161326183574936922
