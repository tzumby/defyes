"""
Stakewise v3 protocol implementation.
The protocol focuses on the osETH token. Currently deployed only on Mainnet.
Docs: https://docs.stakewise.io/
main contracts: https://github.com/stakewise/v3-core/blob/main/deployments/mainnet.json
"""

from karpatkit.constants import Address, Chain

from defyes.functions import ensure_a_block_number
from defyes.protocols.stakewisev3.autogenerated import OsTokenVaultController
from defyes.types import Token, TokenAmount

OsTokenVaultController.default_addresses = {Chain.ETHEREUM: "0x2A261e60FB14586B474C208b1B7AC6D0f5000306"}


def reduce_osETH(amount: int | float, blockchain: str | Chain, block: int | str, teu: bool = False) -> tuple[str, int]:
    """Reduce osETH to ETH.
    Currently the only available blockchain is Ethereum.

    Args:
        amount (float): Amount of osETH to reduce
        block (int | str): Block number or "latest"
        teu (bool, optional): If the amount is in teu. Defaults to False.
    """
    if blockchain != Chain.ETHEREUM:
        raise ValueError("Currently only Ethereum is supported")

    blockchain = ensure_a_block_number(block, blockchain)
    vault_controller = OsTokenVaultController(Chain.ETHEREUM, block)
    token = Token("0xf1C9acDc66974dFB6dEcB12aA385b9cD01190E38", Chain.ETHEREUM, block)

    # In case the amount is in teu just convert it to ETH else convert it to teu and then to ETH
    if teu:
        eth_reduced = vault_controller.convert_to_assets(int(amount))
        eth_reduced = TokenAmount.from_teu(eth_reduced, token).balance(True)

    else:
        amount = TokenAmount(amount, token).balance()
        eth_reduced = vault_controller.convert_to_assets(int(amount))
        eth_reduced = TokenAmount.from_teu(eth_reduced, token).balance(True)

    return Address.ZERO, eth_reduced
