from typing import Union

from moneyed import Money as MoneyedMoney, format_money

from ..decimal import Decimal


class Money(MoneyedMoney):
    def __init__(
        self, amount: Union[int, float, Decimal, MoneyedMoney], currency="INR"
    ):
        super().__init__(amount, currency)

    def format(self):
        return format_money(
            self,
            locale="en_IN",
            format_type="standard",
        )

    def isQuantizedEqual(self, other: "Money"):
        return Decimal(self.amount).isQuantizedEqual(Decimal(other.amount))

    def __float__(self):
        return float(self.amount)

    def __str__(self):
        return self.format()

    def __repr__(self):
        return f"Money({self.format()})"


# if isinstance(amount, MoneyedMoney):
#     self._data = amount
# else:
#     self._data = MoneyedMoney(amount, currency)
