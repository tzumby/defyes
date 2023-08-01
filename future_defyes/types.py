import json
from functools import cached_property

from web3 import Web3

from defi_protocols.cache import const_call
from defi_protocols.constants import ABI_TOKEN_SIMPLIFIED, ZERO_ADDRESS, E_ADDRESS

abi_token_simplified = json.loads(ABI_TOKEN_SIMPLIFIED)


class Addr(str):
    def __new__(cls, addr: int | str, *args, **kwargs):
        if isinstance(addr, str):
            cs_addr = Web3.to_checksum_address(addr)
            if cs_addr != addr:
                raise cls.ChecksumError(f"Provided {addr=!r} differs from expected {cs_addr!r}")
            s = addr
        else:
            s = Web3.to_checksum_address(addr)
        return super().__new__(cls, s)

    class ChecksumError(ValueError):
        pass


class Token(Addr):
    def __init__(self, addr: int | str, label: str):
        self.label = label

    def __repr__(self):
        return f"{self}:{self.label}"


class TokenAmount(int):
    def __new__(cls, value: int, addr: Addr = None, web3: Web3 = None, decimals=None):
        self = super().__new__(cls, value)
        self.addr = addr
        self.web3 = web3
        if decimals is not None:
            self.decimals = decimals
        return self

    @cached_property
    def decimals(self):
        if self.addr == ZERO_ADDRESS or self.addr == E_ADDRESS:
            return 18
        else:
            if self.web3 is None:
                return 0
            token_contract = self.web3.eth.contract(address=self.addr, abi=abi_token_simplified)
            return const_call(token_contract.functions.decimals()) or 0

    def __str__(self):
        if self.decimals == 0:
            return format(int(self), "_")
        str_value = format(int(self))
        integer_part, decimal_part = str_value[: -self.decimals], str_value[-self.decimals :]
        decimal_part = decimal_part.rstrip("0")
        if not decimal_part:
            decimal_part = "0"
        integer_part = f"{int(integer_part):_}"
        return f"{integer_part}.{decimal_part}"

    __repr__ = __str__
