###############################################################################
# 5. Expense
###############################################################################

from decimal import Decimal
from typing import Dict, List, Tuple, TypedDict, Union

from flow_prediction.shared.value_objects.money import Money

from ..base import Aggregate
from ..corpus import Corpus
from flow_prediction.shared.value_objects import Id, InflationAdjustableValue


class FundingCorpus(TypedDict):
    id: Id


class CorporaDeduction(TypedDict):
    corpus: Corpus
    deduction: Money


class Expense(Aggregate):
    """
    Represents an outflow of money (expense):
      - can be recurring (spanning multiple years with growthRate) or lumpsum.
      - lumpsum => only hits in start_year exactly.
      - can have its own growthRate rate (like living expenses,
        which grow yearly).
      - tries to withdraw from corpora in a given priority order.
    """

    def __init__(
        self,
        id: Id,
        startYear: int,
        endYear: int,
        enabled: bool,
        initialValue: InflationAdjustableValue,
        recurringValue: InflationAdjustableValue,
        fundingCorpora: Union[List[FundingCorpus],None],
        corpora: List[Corpus],
        # TODO: account for corpus priority
    ):
        super().__init__(id)
        self.startYear = startYear
        self.endYear = endYear

        self.enabled = enabled
        self.initialValue = initialValue
        self.recurringValue = recurringValue
        self.fundingCorpora: List[FundingCorpus] = fundingCorpora if fundingCorpora is not None else list(map(
            lambda corpus: {"id": corpus.id}, corpora
        ))
        self.validate()

    def validate(self):
        if len(self.fundingCorpora) == 0:
            raise ValueError(f"Expense {self.id} has no funding corpora")

    def isActive(self, year: int) -> bool:
        return self.startYear <= year <= self.endYear and self.enabled

    def getAmountNeeded(self, year) -> Money:
        if not self.isActive(year):
            return Money(0)
        return (
            self.initialValue.getAmount(year)
            if year == self.startYear
            else Money(0)
        ) + self.recurringValue.getAmount(year)

    def _getCorpus(self, corpuses: List[Corpus], id: Id):
        for corpus in corpuses:
            if corpus.id == id:
                return corpus
        raise ValueError(f"Funding Corpus {id} not found for {self}")

    def getCorporaDeductions(
        self, corpuses: List[Corpus], year
    ) -> Tuple[List[CorporaDeduction], List[str]]:
        if not self.isActive(year):
            return ([], [])
        warnings = []
        amountToBeDeducted = self.getAmountNeeded(year)
        deductions = []
        for fundingCorpus in self.fundingCorpora[:-1]:
            corpus = self._getCorpus(corpuses, fundingCorpus["id"])
            corpusDeduction = min(
                corpus.getBalance(),
                amountToBeDeducted,
            )
            deductions.append({"corpus": corpus, "deduction": corpusDeduction})
            amountToBeDeducted -= corpusDeduction
        finalCorpus = self._getCorpus(corpuses, self.fundingCorpora[-1]["id"])
        if amountToBeDeducted > finalCorpus.getBalance():
            warnings.append(
                f"Expense {self.id} in the year {year} overshoots corpora allotment"
            )

        # deduct any remaining amount from the last corpus, even if it doesn't have enough
        deductions.append(
            {"corpus": finalCorpus, "deduction": amountToBeDeducted}
        )
        return (deductions, warnings)

        # return list(map(lambda corpus:self._getCorpusDeductions(corpus['id']),self.fundingCorpora))

    # def amount_for_year(self, year: int) -> Decimal:
    #     """Compute how much we need in 'year' from this expense."""
    #     if not self.isActive(year):
    #         return Decimal("0")
    #     if self.lumpsum and year != self.start_year:
    #         return Decimal("0")
    #     # recurring: apply growthRate
    #     return get_inflated_amount(
    #         self.base_amount, self.inflation_rate, self.start_year, year
    #     )

    # def withdraw(self, year: int, corpora: Dict[str, Corpus]) -> bool:
    #     """
    #     Try to withdraw from corpora in priority order.
    #     Returns True if fully funded, False if partial.
    #     If a corpus goes negative => you can decide to raise
    #     an error or continue.
    #     """
    #     amt = self.amount_for_year(year)
    #     if amt <= 0:
    #         return True

    #     # Attempt in priority order
    #     remaining = amt
    #     for corpus_id in self.corpus_priority:
    #         if remaining <= 0:
    #             break
    #         if corpus_id not in corpora:
    #             continue

    #         # Withdraw from corpus
    #         withdrawn = corpora[corpus_id].withdraw(remaining)
    #         remaining -= withdrawn

    #         # If you want to stop the simulation or raise error if negative:
    #         if corpora[corpus_id].balance < 0:
    #             print(
    #                 f"[ALERT] Corpus '{corpus_id}' is negative after expense"
    #                 f"'{self.name}' in year {year}."
    #             )

    #     # If leftover remains, not fully funded
    #     if remaining > 0:
    #         print(
    #             f"[ALERT] Expense '{self.name}' not fully funded in year {year}. "
    #             f"Shortfall={remaining}"
    #         )
    #         return False

    #     return True
