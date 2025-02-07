# from decimal import Decimal
from typing import Union
from flow_prediction.shared.value_objects import (
    Id,
    InflationAdjustableValue,
    Decimal,
    Money,
)
from ..base import Aggregate


class Corpus(Aggregate):
    """
    A bucket of money that has:
      - a name (id)
      - a current balance
      - an annual growth rate
    """

    def __init__(
        self,
        id: Id,
        growthRate: Decimal,
        initialValue: Money,
        startYear: int,
        endYear: int,
        successCorpusId: Union[Id, None],
    ):
        super().__init__(id)
        self.growthRate = growthRate  # e.g. 0.03 => 3% yearly
        self._balance = initialValue
        self.startYear = startYear
        self.endYear = endYear
        self.successorCorpusId = successCorpusId

    def deposit(self, amount: Money):
        self._balance += amount

    def isGrowing(self, year: int) -> bool:
        return self.startYear <= year <= self.endYear

    def getBalance(self):
        return self._balance

    def withdraw(self, amount: Money):
        """
        Withdraw up to 'amount' from this corpus.
        For simplicity, we always attempt to withdraw the full amount.
        This can drive balance negative if we don't forbid it.
        Return the actual withdrawn amount (same as 'amount'
        in this simple version).
        """
        self._balance -= amount

    def isEnding(self, year: int) -> bool:
        return year == self.endYear

    # def apply_growth(self):
    #     """
    #     Increase the balance by (growth_rate) in a year.
    #     e.g. if growth_rate=0.05 and balance=100, new balance=105
    #     """
    #     self.balance *= Decimal("1") + self.growth_rate

    def __repr__(self):
        return f"<Corpus {self.id}: balance={self._balance:.2f}>"

    def getAnnualAppreciation(self, year):
        if not self.isGrowing(year):
            return Money(0)
        return self._balance * self.growthRate
