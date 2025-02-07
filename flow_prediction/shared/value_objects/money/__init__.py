# from typing import Union
# from moneyed import Money as MoneyedMoney, format_money
# from decimal import Decimal, ROUND_HALF_EVEN


# class Money:
#     _data: MoneyedMoney

#     def __init__(
#         self, amount: Union[int, float, Decimal, MoneyedMoney], currency="INR"
#     ):
#         if isinstance(amount, MoneyedMoney):
#             self._data = amount
#         else:
#             self._data = MoneyedMoney(amount, currency)

#     def __add__(self, other: "Money"):
#         return Money(self._data + other._data)

#     def __sub__(self, other: "Money"):
#         return Money(self._data - other._data)

#     # def __mul__(self, other):
#     #     return Money(self._data * other)

#     def __gt__(self, other: "Money"):
#         return self._data > other._data

#     def __lt__(self, other: "Money"):
#         return self._data < other._data

#     def __eq__(self, other: "Money"):
#         return self._data == other._data

#     def format(self):
#         quantum = Decimal("0.01")
#         try:
#             # Increase precision locally to ensure quantization works for large numbers.
#             with decimal.localcontext() as ctx:
#                 # Set the context precision high enough (50 is arbitrary; choose what fits your needs)
#                 ctx.prec = 50
#                 quantized_amount = self._data.amount.quantize(
#                     quantum, rounding=ROUND_HALF_EVEN
#                 )
#         except Exception as e:
#             raise ValueError(
#                 f"Error quantizing amount {self._data.amount}: {e}"
#             )

#     def __mul__(self, other):
#         if isinstance(other, (int, float, Decimal)):
#             return Money(self._data * Decimal(other))
#         raise TypeError("Cannot multiply Money by a non-numeric type")

#     def __rmul__(self, other):
#         return self.__mul__(other)

#     def __str__(self):
#         return f"{self.format()}"

#     def __repr__(self):
#         return f"<Money {self._data}>"

from typing import Union
from moneyed import Money as MoneyedMoney, format_money
from ..decimal import Decimal


class Money(MoneyedMoney):
    def __init__(
        self, amount: Union[int, float, Decimal, MoneyedMoney], currency="INR"
    ):
        super().__init__(amount, currency)

    def format(self):
        return format_money(self, locale="en_IN")
    def __float__(self):
        return float(self.amount)

# if isinstance(amount, MoneyedMoney):
#     self._data = amount
# else:
#     self._data = MoneyedMoney(amount, currency)
