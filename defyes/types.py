import json
from decimal import Decimal
from functools import cached_property

from web3 import Web3

from .cache import const_call
from .constants import ABI_TOKEN_SIMPLIFIED, Address

abi_token_simplified = json.loads(ABI_TOKEN_SIMPLIFIED)


class Addr:
    def __init__(self, addr: int | str):
        if isinstance(addr, str):
            self.checksum_addr = addr
            self.addr = int(addr, base=16)
            cs_addr = Web3.to_checksum_address(self.addr)
            if cs_addr != self.checksum_addr:
                raise self.ChecksumError(f"Provided {addr=!r} differs from expected {cs_addr!r}")
        else:
            self.addr = addr
            self.checksum_addr = Web3.to_checksum_address(self.addr)

    def __str__(self):
        return self.checksum_addr

    __repr__ = __str__

    def __int__(self):
        return self.addr

    class ChecksumError(ValueError):
        pass


class Token(Addr):
    def __init__(self, addr: int | str, label: str):
        super().__init__(addr)
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
