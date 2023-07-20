from dataclasses import dataclass

from defyes.constants import (
    API_KEY_ARBITRUM,
    API_KEY_AVALANCHE,
    API_KEY_BINANCE,
    API_KEY_ETHERSCAN,
    API_KEY_FANTOM,
    API_KEY_GNOSISSCAN,
    API_KEY_POLSCAN,
    Chain,
)
from defyes.enums import Explorer

blockexplorers = {
    Chain.ETHEREUM: [Explorer.ETHERSCAN.value, API_KEY_ETHERSCAN],
    Chain.POLYGON: [Explorer.POLYSCAN.value, API_KEY_POLSCAN],
    Chain.GNOSIS: [Explorer.GNOSISSCAN.value, API_KEY_GNOSISSCAN],
    Chain.GNOSIS: [Explorer.GNOSISSCAN.value, API_KEY_GNOSISSCAN],
    Chain.BINANCE: [Explorer.BSCSCAN.value, API_KEY_BINANCE],
    Chain.AVALANCHE: [Explorer.AVAXSCAN.value, API_KEY_AVALANCHE],
    Chain.FANTOM: [Explorer.FTMSCAN.value, API_KEY_FANTOM],
    Chain.ARBITRUM: [Explorer.ARBISCAN.value, API_KEY_ARBITRUM],
}


# FIXME: this collides with the imported Explorer
@dataclass
class Explorer:
    blockchain: str

    def get_explorer(self):
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[0]

    def get_private_key(self):
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[1]
