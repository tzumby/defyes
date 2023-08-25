from dataclasses import dataclass
from decimal import Decimal
from typing import ClassVar


class ProtocolDataError(Exception):
    pass


@dataclass
class ProtocolData:
    VERSION: ClassVar[int] = 0
    POSITION_TYPES: ClassVar[list] = ["liquidity", "staked", "locked", "financial_metrics"]

    protocol: str
    blockchain: str
    block: str | int
    positions_key: str

    def __post_init__(self):
        self.positions = {}
        self.version = self.VERSION

    @property
    def position_item(self):
        return {key: {} for key in self.POSITION_TYPES}

    def _check_position_type(self, position_type):
        return position_type in self.POSITION_TYPES

    def add_holding(
        self,
        key: str,
        position_type: str,
        addr: str,
        balance: Decimal,
        extra_level: str = None,
        extra_level_type: str = None,
    ) -> None:
        self._add_to_position(key, position_type, addr, balance, "holdings", extra_level, extra_level_type)

    def add_underlying(
        self,
        key: str,
        position_type: str,
        addr: str,
        balance: Decimal,
        extra_level: str = None,
        extra_level_type: str = None,
    ) -> None:
        self._add_to_position(key, position_type, addr, balance, "underlyings", extra_level, extra_level_type)

    def add_reward(
        self,
        key: str,
        position_type: str,
        addr: str,
        balance: Decimal,
        extra_level: str = None,
        extra_level_type: str = None,
    ) -> None:
        self._add_to_position(key, position_type, addr, balance, "unclaimed_rewards", extra_level, extra_level_type)

    def _add_to_position(
        self,
        key: str,
        position_type: str,
        addr: str,
        balance: Decimal,
        field: str,
        extra_level: str = None,
        extra_level_type: str = None,
    ) -> None:
        if balance:
            self.positions[key] = self.positions.get(key, self.position_item)
            assert self._check_position_type(position_type)
            d = self.positions[key][position_type]
            if extra_level:
                level_type = d.get(f"{position_type}_key", None)
                if not level_type:
                    d[f"{position_type}_key"] = extra_level_type
                elif level_type != extra_level_type:
                    raise ProtocolDataError(
                        f"Trying to set {extra_level_type}:{position_type} can have only one {position_type}_key. Actual: {level_type}"
                    )

                d[extra_level] = d.get(extra_level, {})
                d = d[extra_level]

            d[field] = d.get(field, [])
            d[field].append({"address": addr, "balance": balance})

    @property
    def as_dict(self):
        return self.__dict__
