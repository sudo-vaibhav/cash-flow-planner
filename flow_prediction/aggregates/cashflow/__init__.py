from typing import List, TypedDict
from .allocation import Allocation
from flow_prediction.shared.value_objects import InflationAdjustableValue, Id
from ..base import Aggregate


class CashflowInitData(TypedDict):
    id: Id
    recurringValue: InflationAdjustableValue
    enabled: bool
    startYear: int
    endYear: int
    allocations: List[Allocation]
    expandedDescription: str


class Cashflow(Aggregate):
    """
    A strictly positive flow (e.g., salary, rental income) with a
    start/end year and growthRate.
    Example:
      - name = "Salary2025"
      - base_amount = 800000 (in year = start_year)
      - start_year = 2025
      - end_year = 2030
      - inflation_rate = 0.05 (5% yearly)
    """

    Allocation = Allocation

    def __init__(
        self,
        data: CashflowInitData,
    ):
        super().__init__(data["id"])
        self.recurringValue = data["recurringValue"]
        self.startYear = data["startYear"]
        self.enabled = data["enabled"]
        self.endYear = data["endYear"]
        self._allocations = data["allocations"]
        self.expandedDescription = data["expandedDescription"]
        self.validate()

    @property
    def hasValidAllocations(self):
        # check for no overlap between allocations
        for i, allocation in enumerate(self._allocations):
            for other_allocation in self._allocations[i + 1 :]:
                if allocation.overlaps(other_allocation):
                    return False
        return True

    def validate(self):
        if not self.hasValidAllocations:
            raise ValueError(f"Invalid allocations for cashflow {self.id}")

    def is_active(self, year: int) -> bool:
        """Check if this flow is active in a given year."""
        return self.startYear <= year <= self.endYear and self.enabled

    def getAllocation(self, year: int):
        if not self.is_active(year):
            return None
        for allocation in self._allocations:
            if allocation.startYear <= year <= allocation.endYear:
                return allocation
        return None

    def getAmount(self, year: int):
        return self.recurringValue.getAmount(year)


# __all__ = ["Cashflow", "Allocation"]
