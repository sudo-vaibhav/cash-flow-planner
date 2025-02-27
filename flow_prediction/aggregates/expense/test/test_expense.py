import pytest

from flow_prediction.shared.value_objects import InflationAdjustableValue, Id
from flow_prediction.shared.value_objects.money import Money
# Adjust the following import to your project’s structure.
from .. import Expense, FundingCorpus


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

    def __eq__(self, other):
        return (
            isinstance(other, FakeCorpus)
            and self.id == other.id
            and self._balance == other._balance
        )


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
            id=Id("exp1"),
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
    funding = [FundingCorpus(Id("c1"), startYear=2025, forInitialOnly=False)]
    expense = Expense(
        id=Id("exp1"),
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
        id=Id("exp2"),
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
    For a disabled expense on its start year, the new behavior is that:
      - getInitialAmountNeeded returns the initial value (since it only checks the year)
      - getRecurringAmountNeeded returns Money(0) (because the expense is not active)
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 100)
    funding = [FundingCorpus(Id("c1"), startYear=2025, forInitialOnly=False)]
    expense = Expense(
        id=Id("exp1"),
        startYear=2025,
        endYear=2030,
        enabled=False,  # disabled expense
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    assert expense.getInitialAmountNeeded(2025) == Money(100)
    assert expense.getRecurringAmountNeeded(2025) == Money(0)


def test_getAmountNeeded_start_year():
    """
    On the start year of an enabled expense:
      - getInitialAmountNeeded returns the initial value
      - getRecurringAmountNeeded returns the recurring value
    For example, if initialValue(2025)=100 and recurringValue(2025)=10,
    then the combined needed amount is 110.
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 200)
    funding = [FundingCorpus(Id("c1"), startYear=2025, forInitialOnly=False)]
    expense = Expense(
        id=Id("exp1"),
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    total_needed = expense.getInitialAmountNeeded(
        2025
    ) + expense.getRecurringAmountNeeded(2025)
    # Expected: 100 + 10 = 110
    assert total_needed == Money(110)


def test_getAmountNeeded_non_start_year():
    """
    In a non-start active year, only the recurring value applies.
    For example, if recurringValue(2026)=20, then the needed amount is 20.
    """
    initial = FakeInflationAdjustableValue({2025: 100, 2026: 100})
    recurring = FakeInflationAdjustableValue({2026: 20})
    corpus = FakeCorpus("c1", 200)
    funding = [FundingCorpus(Id("c1"), startYear=2025, forInitialOnly=False)]
    expense = Expense(
        id=Id("exp1"),
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus],
    )
    total_needed = expense.getInitialAmountNeeded(
        2026
    ) + expense.getRecurringAmountNeeded(2026)
    # Expected: initial is 0 in non-start year, recurring is 20.
    assert total_needed == Money(20)


def test_getCorporaDeductions_inactive():
    """
    If the expense is inactive, getCorporaDeductions should return an empty list and None for violation.
    """
    initial = FakeInflationAdjustableValue({2025: 100})
    recurring = FakeInflationAdjustableValue({2025: 10})
    corpus = FakeCorpus("c1", 200)
    funding = [FundingCorpus(Id("c1"), startYear=2025, forInitialOnly=False)]
    expense = Expense(
        id=Id("exp1"),
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
    For an active expense in the start year with:
      - initialValue=20 and recurringValue=30 (total needed = 50),
      - Two funding corpora (corpus "c1" and corpus "c2").
    With the new two-loop deduction process, the non-final funding corpus (corpus1)
    is used in both the initial and recurring loops. In this configuration:
      - In the initial loop, corpus1 contributes min(Money(30), Money(20)) = Money(20)
      - In the recurring loop, corpus1 contributes min(Money(30), Money(30)) = Money(30)
      - The final funding corpus (corpus2) then gets the remaining 0.
    No violation should be flagged.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    corpus1 = FakeCorpus("c1", 30)
    corpus2 = FakeCorpus("c2", 40)
    funding = [
        FundingCorpus(Id("c1"), startYear=None, forInitialOnly=False),
        FundingCorpus(Id("c2"), startYear=None, forInitialOnly=False),
    ]
    expense = Expense(
        id=Id("exp1"),
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus1, corpus2],
    )
    deductions, violated = expense.getCorporaDeductions([corpus1, corpus2], 2025)

    # Expected deductions according to the new implementation:
    # 1. From corpus1 in the initial loop: Money(20)
    # 2. From corpus1 in the recurring loop: Money(30)
    # 3. From corpus2 (final corpus): Money(0)
    assert len(deductions) == 3
    assert deductions[0]["corpus"] == corpus1
    assert deductions[0]["deduction"] == Money(20)
    assert deductions[1]["corpus"] == corpus1
    assert deductions[1]["deduction"] == Money(30)
    assert deductions[2]["corpus"] == corpus2
    assert deductions[2]["deduction"] == Money(0)
    assert violated is None


def test_getCorporaDeductions_violation():
    """
    When the non-final funding corpora are skipped (using startYear restrictions),
    the entire amount (initial + recurring) falls on the final funding corpus.
    If that corpus’s balance is insufficient, a ValueError should be raised.
    For example, if total needed is Money(50) but the final corpus has only Money(10),
    then a ValueError is raised.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    # The first funding corpus is skipped because its startYear is in the future.
    corpus1 = FakeCorpus("c1", 100)
    corpus2 = FakeCorpus("c2", 10)  # insufficient balance for final corpus
    funding = [
        FundingCorpus(Id("c1"), startYear=2030, forInitialOnly=False),
        FundingCorpus(Id("c2"), startYear=None, forInitialOnly=False),
    ]
    expense = Expense(
        id=Id("exp1"),
        startYear=2025,
        endYear=2030,
        enabled=True,
        initialValue=initial,
        recurringValue=recurring,
        fundingCorpora=funding,
        corpora=[corpus1, corpus2],
    )
    with pytest.raises(ValueError, match="doesn't have"):
        expense.getCorporaDeductions([corpus1, corpus2], 2025)


def test_getCorporaDeductions_with_startYear_skip():
    """
    If a funding corpus has a startYear later than the current year,
    it should be skipped. Only the final funding corpus (with no startYear restriction)
    will be used to cover the full amount.
    For example, if total needed is Money(50) in 2025 and the first funding corpus is
    skipped, then corpus "c2" should cover the entire amount.
    """
    initial = FakeInflationAdjustableValue({2025: 20})
    recurring = FakeInflationAdjustableValue({2025: 30})
    corpus1 = FakeCorpus("c1", 30)
    corpus2 = FakeCorpus("c2", 60)
    # "c1" has a startYear of 2030, so it will be skipped in 2025.
    funding = [
        FundingCorpus(Id("c1"), startYear=2030, forInitialOnly=False),
        FundingCorpus(Id("c2"), startYear=None, forInitialOnly=False),
    ]
    expense = Expense(
        id=Id("exp1"),
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
