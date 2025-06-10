from enum import Enum
from enums import Convert, Symbol


class TargetPriceCondition(Enum):
    LOWER = 0
    HIGHER = 1


class Alert:
    target_price: float
    condition: TargetPriceCondition
    symbol: Symbol
    convert: Convert
    __is_notified: bool = False

    def __init__(
        self,
        target_price: float,
        condition: TargetPriceCondition,
        symbol: Symbol,
        convert: Convert,
    ):
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
            target_price=data["target_price"],
            condition=TargetPriceCondition[data["condition"]],
            symbol=Symbol[data["symbol"]],
            convert=Convert[data["convert"]],
        )
