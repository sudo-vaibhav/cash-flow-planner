from ..decimal import Decimal
from ..money import Money


class InflationAdjustableValue:
    _amount: Money
    referenceTime: int
    growthRate: Decimal

    def __init__(self, amount: Money, referenceTime: int, growthRate: Decimal):
        self._amount = amount
        self.referenceTime = referenceTime
        self.growthRate = growthRate

    def validate(self):
        if self.growthRate < 0 or self.growthRate > 1:
            raise ValueError(
                f"Growth rate {self.growthRate} should be between 0 and 1"
            )

    def getAmount(self, year: int):
        """
        Returns the value of the amount at the given year.
        """
        if year < self.referenceTime:
            raise ValueError(
                f"Year {year} for amount calculation is before the reference"
                f"time {self.referenceTime}"
            )
        return self._amount * (
            (1 + self.growthRate) ** (year - self.referenceTime)
        )
