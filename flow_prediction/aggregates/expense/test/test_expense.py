import pytest

from flow_prediction.shared.value_objects import InflationAdjustableValue, Id
from flow_prediction.shared.value_objects.money import Money

# Adjust the following import to your project’s structure.
from .. import Expense


# =============================================================================
# Fake implementations for testing (do not mock Money)
# =============================================================================


class FakeInflationAdjustableValue(InflationAdjustableValue):
    """
    A simple implementation of InflationAdjustableValue for testing.
    It accepts a dictionary mapping years to a numeric amount.
    """

    def __init__(self, amounts: dict):
        self.amounts = amounts  # e.g. {2025: 100, 2026: 110}

    def getAmount(self, year: int) -> Money:
        return Money(self.amounts.get(year, 0))


class FakeCorpus:
    """
    A minimal fake corpus that exposes an 'id' attribute and a getBalance method.
    """

    def __init__(self, id: str, balance: float, startYear: int = None):
        self.id = Id(id)
        self._balance = balance
        self.startYear = startYear

    def getBalance(self) -> Money:
        return Money(self._balance)


# =============================================================================
# Tests for Expense
# =============================================================================


def test_validate_empty_funding_corpora():
    """
    An Expense must have at least one funding corpus.
    When fundingCorpora is explicitly empty, validate() should raise a ValueError.
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 100)
    with pytest.raises(ValueError, match="has no funding corpora"):
        Expense(
            id="exp1",
            startYear=2025,
            endYear=2030,
            enabled=True,
            initialValue=initial,
            recurringValue=recurring,
            fundingCorpora=[],  # explicitly empty funding list
            corpora=[corpus],
        )


def test_isActive():
    """
    Test that isActive returns True when the expense is enabled and within its active period,
    and False otherwise.
    """
    initial = FakeInflationAdjustableValue({2025: 50})
    recurring = FakeInflationAdjustableValue({2025: 5})
    corpus = FakeCorpus("c1", 100)
    funding = [{"id": "c1", "startYear": 2025}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    # Active within period
    assert expense.isActive(2025) is True
    assert expense.isActive(2030) is True
    # Outside active period
    assert expense.isActive(2024) is False

    # Disabled expense is never active.
    expense_disabled = Expense(
        id="exp2",
        startYear=2025,
        endYear=2030,
        enabled=False,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    assert expense_disabled.isActive(2027) is False


def test_getAmountNeeded_inactive():
    """
    When the expense is inactive, getAmountNeeded should return Money(0).
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 100)
    funding = [{"id": "c1", "startYear": 2025}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=False,  # disabled expense
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    amount = expense.getAmountNeeded(2025)
    assert amount == Money(0)


def test_getAmountNeeded_start_year():
    """
    On the start year, getAmountNeeded should sum the initial and recurring values.
    For example, if initialValue(2025)=100 and recurringValue(2025)=10,
    then the needed amount is 110.
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 200)
    funding = [{"id": "c1", "startYear": 2025}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    amount = expense.getAmountNeeded(2025)
    # Expected: initial + recurring = Money(100) + Money(10) = Money(110)
    assert amount == Money(110)


def test_getAmountNeeded_non_start_year():
    """
    In a non-start active year, only the recurring value applies.
    For example, if recurringValue(2026)=20, then the needed amount is 20.
    """
    initial = FakeInflationAdjustableValue({2025: 100, 2026: 100})
    recurring = FakeInflationAdjustableValue({2026: 20})
    corpus = FakeCorpus("c1", 200)
    funding = [{"id": "c1", "startYear": 2025}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    amount = expense.getAmountNeeded(2026)
    # Expected: Money(0) from initial (since not start year) + Money(20)
    assert amount == Money(20)


def test_getCorporaDeductions_inactive():
    """
    If the expense is inactive, getCorporaDeductions should return an empty list and None for violation.
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 200)
    funding = [{"id": "c1", "startYear": 2025}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=False,  # inactive
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    deductions, violated = expense.getCorporaDeductions([corpus], 2025)
    assert deductions == []
    assert violated is None


def test_getCorporaDeductions_normal():
    """
    For an active expense where:
      - In the start year, initialValue=20 and recurringValue=30 (total needed = 50).
      - Two funding corpora: corpus "c1" with balance 30, corpus "c2" with balance 40.
    The first funding corpus should contribute Money(30) and the final corpus Money(20).
    No violation should be flagged.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    corpus1 = FakeCorpus("c1", 30)
    corpus2 = FakeCorpus("c2", 40)
    funding = [{"id": "c1"}, {"id": "c2"}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus1, corpus2],
    )
    deductions, violated = expense.getCorporaDeductions([corpus1, corpus2], 2025)

    # Expect first deduction: min(Money(30), Money(50)) = Money(30)
    # Remaining: Money(20) from corpus2.
    assert len(deductions) == 2
    assert deductions[0]["corpus"] == corpus1
    assert deductions[0]["deduction"] == Money(30)
    assert deductions[1]["corpus"] == corpus2
    assert deductions[1]["deduction"] == Money(20)
    assert violated is None


def test_getCorporaDeductions_violation():
    """
    When the final funding corpus does not have sufficient balance,
    the method should still add the final deduction but also flag a violation.
    For example, if:
      - Total needed = Money(50) (from initial=20 and recurring=30),
      - corpus "c1" provides Money(30),
      - corpus "c2" has balance Money(10),
    then after corpus "c1" the remaining amount is Money(20), which exceeds corpus "c2" balance.
    The final deduction is Money(20) and corpus "c2" is flagged as violated.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    corpus1 = FakeCorpus("c1", 30)
    corpus2 = FakeCorpus("c2", 10)
    funding = [{"id": "c1"}, {"id": "c2"}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus1, corpus2],
    )
    deductions, violated = expense.getCorporaDeductions([corpus1, corpus2], 2025)
    assert len(deductions) == 2
    # corpus "c1" provides Money(30)
    assert deductions[0]["corpus"] == corpus1
    assert deductions[0]["deduction"] == Money(30)
    # Final funding corpus "c2" is used for the remaining Money(20)
    assert deductions[1]["corpus"] == corpus2
    assert deductions[1]["deduction"] == Money(20)
    # Since corpus "c2" had only Money(10) available, it is flagged as violated.
    assert violated == corpus2


def test_getCorporaDeductions_with_startYear_skip():
    """
    If a funding corpus has a startYear later than the current year,
    it should be skipped. Only the final funding corpus (which has no startYear restriction)
    should be used.
    For example, if:
      - Total needed = Money(50) (from initial=20 and recurring=30) in year 2025,
      - Funding corpora: first corpus "c1" with startYear=2030 (skipped) and final corpus "c2" (used),
      - corpus "c2" has sufficient balance,
    then only corpus "c2" is used for the full amount.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    corpus1 = FakeCorpus("c1", 30)
    corpus2 = FakeCorpus("c2", 60)
    # Note: "c1" has a startYear of 2030, so in year 2025 it will be skipped.
    funding = [{"id": "c1", "startYear": 2030}, {"id": "c2"}]
    expense = Expense(
        id="exp1",
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus1, corpus2],
    )
    deductions, violated = expense.getCorporaDeductions([corpus1, corpus2], 2025)
    # Since the first funding corpus is skipped, only the final one is used.
    assert len(deductions) == 1
    assert deductions[0]["corpus"] == corpus2
    assert deductions[0]["deduction"] == Money(50)
    assert violated is None
