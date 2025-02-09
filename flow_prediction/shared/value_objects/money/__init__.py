from typing import Union
from moneyed import Money as MoneyedMoney, format_money

# import decimal
from ..decimal import Decimal


class Money(MoneyedMoney):
    def __init__(
        self, amount: Union[int, float, Decimal, MoneyedMoney], currency="INR"
    ):
        super().__init__(amount, currency)

    def format(self):
        return format_money(self, locale="en_IN")

    def isQuantizedEqual(self, other: "Money"):
        return Decimal(self.amount).isQuantizedEqual(Decimal(other.amount))

    def __float__(self):
        return float(self.amount)


# if isinstance(amount, MoneyedMoney):
#     self._data = amount
# else:
#     self._data = MoneyedMoney(amount, currency)
