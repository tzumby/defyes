from decimal import Decimal
from functools import cached_property

from web3 import Web3

from .cache import cache_token
from .constants import Address, Chain
from .contracts import Erc20

simple_repr = False


class Addr(str):
    # TODO: Maybe move chain to Addr
    def __new__(cls, addr: int | str, *args, **kwargs):
        if isinstance(addr, str):
            int_addr = int(addr, base=16)
            cs_addr = Web3.to_checksum_address(int_addr)
            if cs_addr != addr:
                raise cls.ChecksumError(f"Provided {addr=!r} differs from expected {cs_addr!r}")
            s = addr
        else:
            s = Web3.to_checksum_address(addr)
        return super().__new__(cls, s)

    class ChecksumError(ValueError):
        pass


class Token(Addr):
    def __init__(self, addr: int | str, chain: Chain = Chain.ETHEREUM, **kwargs):
        self.chain = chain

    def __hash__(self):
        return hash((str(self), self.chain))

    @cached_property
    def symbol(self):
        return self.contract.symbol

    def __repr__(self):
        if simple_repr:
            return self.symbol
        else:
            return f"{self.__class__.__name__}({str(self)!r}, {self.chain!r}, symbol={self.symbol!r})"

    @cached_property
    def contract(self):
        return Erc20(self.chain, "latest", self)  # TODO: "latest" or a fixed block_id

    @cached_property
    def decimals(self):
        if self == Address.ZERO or self == Address.E:
            return 18
        else:
            return self.contract.decimals

    @classmethod
    def get_instance(cls, addr: int | str, chain: Chain = Chain.ETHEREUM):
        """
        Return the cached token, otherwise create a new instance and cache it.
        """
        return cls(addr, chain)  # TODO: Fix cache_token and check if cached_property is cached

        try:
            return cache_token[addr, chain]
        except KeyError:
            cache_token[addr, chain] = (token := cls(addr, chain))
            return token

    def __rmul__(self, left_value):
        if isinstance(left_value, str):
            value = Decimal(left_value).scaleb(self.decimals)
            if int(value) != value:
                raise ValueError(
                    f"Preventing str precision loss. {left_value} has more decimals than this token ({self.decimals} decimals)."
                )
        elif isinstance(left_value, Decimal):
            value = left_value.scaleb(self.decimals)
            if int(value) != value:
                raise ValueError(
                    f"Preventing Decimal precision loss. {left_value} has more decimals than this token ({self.decimals} decimals)."
                )
        elif isinstance(left_value, int):
            value = left_value * 10**self.decimals
        elif isinstance(left_value, float):
            raise ValueError("Preventing potential float precision loss. Use str, Decimal or int instead.")
        else:
            raise ValueError(f"{type(left_value)} not sopported in convetion to a TokenAmount value.")
        return TokenAmount(int(value), self)


class TokenAmount(int):
    def __new__(cls, value: int, token: Token, *args, **kwargs):
        self = super().__new__(cls, value)
        self.token = token
        return self

    def __str__(self):
        decimals = self.token.decimals
        if decimals == 0:
            return format(int(self), "_")
        str_value = format(int(self))
        integer_part, decimal_part = str_value[:-decimals], str_value[-decimals:]
        decimal_part = decimal_part.rstrip("0")
        if not decimal_part:
            decimal_part = "0"
        integer_part = f"{int(integer_part):_}"
        return f"{integer_part}.{decimal_part}"

    def __repr__(self):
        if simple_repr:
            return f"{str(self)!r}*{self.token.symbol}"
        else:
            return f"{self.__class__.__name__}({int(self)}, {repr(self.token)})"
