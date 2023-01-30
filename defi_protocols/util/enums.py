"""Location of all Enum types"""

from enum import Enum
import os


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))



class Chain(ExtendedEnum):
    """Enum for the blockchain"""

    ETHEREUM = 'ethereum'
    POLYGON = 'polygon'
    GNOSIS = 'gnosis'
    ARBITRUM = 'arbitrum'
    BINANCE = 'binance'
    AVALANCHE = 'avalanche'
    FANTOM = 'fantom'
    OPTIMISM = 'optimism'
    AVAX = 'avax'
    ROPSTEN = 'ropsten'
    KOVAN = 'kovan'
    GOERLI = 'goerli'

    def __str__(self) -> str:
        """Represent as string."""
        return self.name

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self)

class Explorer(ExtendedEnum):
    """Enum for the blockexplorers"""

    ETHERSCAN = 'etherscan'
    POLYSCAN = 'polyscan'
    GNOSISSCAN = 'gnosisscan'
    BSCSCAN = 'bscscan'
    AVAXSCAN = 'snowtrace'
    FTMSCAN = 'ftmscan'

    def __str__(self) -> str:
        """Represent as string."""
        return self.name

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self)




