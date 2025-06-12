from enum import Enum
from enums import Convert, Symbol
from uuid import UUID

class TargetPriceCondition(Enum):
    LOWER = 0
    HIGHER = 1


class Alert:
    id: UUID
    target_price: float
    condition: TargetPriceCondition
    symbol: Symbol
    convert: Convert
    __is_notified: bool = False

    def __init__(
        self,
        id: UUID,
        target_price: float,
        condition: TargetPriceCondition,
        symbol: Symbol,
        convert: Convert,
    ):
        self.id = id
        self.target_price = target_price
        self.condition = condition
        self.symbol = symbol
        self.convert = convert

    def is_notified(self) -> bool:
        return self.__is_notified

    def set_notified(self):
        self.__is_notified = True

    @classmethod
    def from_dict(cls, data):
        return cls(
            UUID(data["id"]),
            data["target_price"],
            TargetPriceCondition[data["condition"]],
            Symbol[data["symbol"]],
            Convert[data["convert"]],
        )
