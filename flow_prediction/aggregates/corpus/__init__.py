# from decimal import Decimal
from typing import Union

from flow_prediction.shared.value_objects import (
    Id,
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

    def conductAnnualAppreciation(self, year: int):
        appreciatedAmount = self._getAnnualAppreciation(year)
        if appreciatedAmount.isQuantizedEqual(Money(0)):
            return
        print(
            f"Conducting annual appreciation for corpus {self.id} in year {year} with amount {float(appreciatedAmount.amount)}"
        )
        self._balance += appreciatedAmount

    def deposit(self, amount: Money, year: int):
        if not self.isActive(year):
            raise ValueError(
                f"Corpus {self.id} is not active in year {year}, hence cannot deposit, only grow"
            )
        self._balance += amount

    def transferAllTo(self, target, year):
        if not isinstance(target, Corpus):
            raise ValueError(f"Target must be a Corpus")
        print(
            f"Transferring the entire corpus value {float(self._balance.amount)} from {self.id} to {target.id}"
        )
        balance = self.getBalance()
        self.withdraw(balance, year)
        target.deposit(balance, year)

    def isActive(self, year: int) -> bool:
        return self.startYear <= year <= self.endYear

    def getBalance(self):
        return self._balance

    def getInflationAdjustedBalance(
        self, currentYear, baseYear: int, baseInflation: Decimal
    ):
        return self._balance / (
            (1 + baseInflation) ** (currentYear - baseYear)
        )

    def withdraw(self, amount: Money, year: int):
        """
        Withdraw up to 'amount' from this corpus.
        For simplicity, we always attempt to withdraw the full amount.
        This can drive balance negative if we don't forbid it.
        Return the actual withdrawn amount (same as 'amount'
        in this simple version).
        """
        # if not self.isActive(year):
        #     raise ValueError(f"Corpus {self.id} is not active in year {year}, hence cannot withdraw")
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

    def _getAnnualAppreciation(self, year):
        # if not self.isActive(year):
        #     return Money(0)
        return self._balance * self.growthRate
