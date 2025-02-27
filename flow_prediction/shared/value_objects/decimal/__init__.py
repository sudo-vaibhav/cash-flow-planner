from decimal import Decimal as BaseDecimal, getcontext, ROUND_HALF_UP

getcontext().prec = 28  # sets precision to 6 significant digits
# target_precision = BaseDecimal('1.000000000000')  # This pattern represents 12 decimal places


class Decimal(BaseDecimal):
    # Define a default target precision (here, two decimal places).
    default_precision = BaseDecimal("0.01")

    def isQuantizedEqual(self, other, target_precision=None):
        """
        Compare self and other after quantizing both to a target precision.

        :param other: The other value to compare (can be a Decimal or a value convertible to Decimal)
        :param target_precision: A Decimal representing the quantization target, e.g., Decimal('0.01')
                                 If None, the class's default_precision is used.
        :return: True if the quantized values are equal, False otherwise.
        """
        # Use default precision if none is provided.
        if target_precision is None:
            target_precision = self.default_precision

        # Quantize self using the given target precision.
        quantized_self = self.quantize(target_precision, rounding=ROUND_HALF_UP)

        # Ensure 'other' is a Decimal. If not, convert it.
        if not isinstance(other, BaseDecimal):
            other = Decimal(other)
        quantized_other = other.quantize(target_precision, rounding=ROUND_HALF_UP)
        return quantized_self == quantized_other

    def __add__(self, other):
        result = super().__add__(other)
        return self.__class__(result)

    def __radd__(self, other):
        result = super().__radd__(other)
        return self.__class__(result)


#
#
# class Decimal:
#     # def __sum__(self, other):
#     #
#     #     return Decimal(self._value + other)
#
#     def quantizedComparison(self, other):
#         quantizedSelf = self._value.quantize(target_precision)
#         quantizedOther = other.quantize(target_precision)
#         return quantizedSelf == quantizedOther
#     def quantize(self):
#         return Decimal(self._value.quantize(target_precision))
#     def __sub__(self, other):
#         return Decimal(self._value - DecimalLib(other))
#     def __mul__(self, other):
#         return Decimal(self._value * DecimalLib(other))
#     def __truediv__(self, other):
#         return Decimal(self._value / DecimalLib(other))
#     def __init__.py(self, value):
#         if isinstance(value, DecimalLib):
#             self._value = value
#         else:
#             self._value = DecimalLib(value)
#     def __add__(self, other):
#         return Decimal(self._value + other)
#     def __radd__(self, other):
#         return Decimal(self._value + other)
#     def __sum__(self, other):
#         return Decimal(self._value + other)
