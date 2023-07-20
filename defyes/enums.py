"""Location of all Enum types"""

from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Explorer(ExtendedEnum):
    """Enum for the blockexplorers"""

    ETHERSCAN = "etherscan.io"
    POLYSCAN = "polygonscan.com"
    GNOSISSCAN = "gnosisscan.io"
    BSCSCAN = "bscscan.com"
    AVAXSCAN = "snowtrace.io"
    FTMSCAN = "ftmscan.io"
    ARBISCAN = "arbisscan.io"

    def __str__(self) -> str:
        """Represent as string."""
        return self.name

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self)
