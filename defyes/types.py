import json
from decimal import Decimal
from functools import cached_property

from web3 import Web3

from .cache import const_call
from .constants import ABI_TOKEN_SIMPLIFIED, Address

abi_token_simplified = json.loads(ABI_TOKEN_SIMPLIFIED)


class Addr(str):
    def __new__(cls, addr: int | str, *args, **kwargs):
        if isinstance(addr, Addr):
            return addr
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
    def __init__(self, addr: int | str, label: str):
        self.label = label

    def __repr__(self):
        return f"{self.label}:{self.__class__.__name__}"


class Contract(Token):
    pass


class TokenAmount(int):
    def __new__(cls, value: int, addr: Addr, web3: Web3):
        self = super().__new__(value)
        self.addr = addr
        self.web3 = web3
        return self

    @cached_property
    def decimal(self):
        return Decimal(self).scaleb(-self.decimals)

    @cached_property
    def decimals(self):
        if self.addr == Address.ZERO or self.addr == Address.E:
            return 18
        else:
            token_contract = self.web3.eth.contract(address=self.addr, abi=abi_token_simplified)
            return const_call(token_contract.functions.decimals()) or 0

    def __repr__(self):
        return repr(self.decimal)
