from typing import List, Tuple, TypedDict, Union

from flow_prediction.shared.value_objects import Id, InflationAdjustableValue
from flow_prediction.shared.value_objects.money import Money
from ..base import Aggregate
from ..corpus import Corpus


class FundingCorpus:
    id: Id
    startYear: Union[int, None]
    forInitialOnly: bool

    def isAllowedToFund(self, year: int, expenseType) -> bool:
        if self.startYear is None or self.startYear <= year:
            if expenseType == "recurring":
                return self.forInitialOnly == False
            else:
                return True
        else:
            return False

    def __init__(self, id: Id, startYear: Union[int, None], forInitialOnly: bool):
        self.id = id
        self.startYear = startYear
        self.forInitialOnly = forInitialOnly


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
        fundingCorpora: Union[List[FundingCorpus], None],
        corpora: List[Corpus],
        # TODO: account for corpus priority
    ):
        super().__init__(id)
        self.startYear = startYear
        self.endYear = endYear

        self.enabled = enabled
        self.initialValue = initialValue
        self.recurringValue = recurringValue
        self.fundingCorpora: List[FundingCorpus] = (
            fundingCorpora
            if fundingCorpora is not None
            else list(
                map(
                    lambda corpus: {
                        "id": corpus.id,
                        startYear: corpus.startYear,
                    },
                    corpora,
                )
            )
        )
        self.validate()

    def validate(self):
        if len(self.fundingCorpora) == 0:
            raise ValueError(f"Expense {self.id} has no funding corpora")

    def isActive(self, year: int) -> bool:
        return self.startYear <= year <= self.endYear and self.enabled

    def getInitialAmountNeeded(self, year) -> Money:
        return self.initialValue.getAmount(year) if year == self.startYear else Money(0)

    def getRecurringAmountNeeded(self, year) -> Money:
        if not self.isActive(year):
            return Money(0)
        return self.recurringValue.getAmount(year)

    # @deprecated
    # def getAmountNeeded(self, year) -> Money:
    #     if not self.isActive(year):
    #         return Money(0)
    #     return (
    #         self.initialValue.getAmount(year) if year == self.startYear else Money(0)
    #     ) + self.recurringValue.getAmount(year)

    def _getCorpus(self, corpora: List[Corpus], id: Id):
        for corpus in corpora:
            if corpus.id == id:
                return corpus
        raise ValueError(f"Funding Corpus {id} not found for {self}")

    def getCorporaDeductions(
        self, corpora: List[Corpus], year
    ) -> Tuple[List[CorporaDeduction], Union[Corpus, None]]:
        if not self.isActive(year):
            return ([], None)
        print(f"Calculating deductions for {self.id} in {year}")
        violatedCorpus: Union[Corpus, None] = None
        deductions = []
        initialAmountToBeDeducted = self.getInitialAmountNeeded(year)
        for fundingCorpus in self.fundingCorpora[:-1]:
            if fundingCorpus.isAllowedToFund(year, "initial"):
                corpus = self._getCorpus(corpora, fundingCorpus.id)
                corpusDeduction = min(
                    corpus.getBalance(),
                    initialAmountToBeDeducted,
                )
                deductions.append({"corpus": corpus, "deduction": corpusDeduction})
                initialAmountToBeDeducted -= corpusDeduction
        recurringAmountToBeDeducted = self.getRecurringAmountNeeded(year)
        for fundingCorpus in self.fundingCorpora[:-1]:
            if fundingCorpus.isAllowedToFund(year, "recurring"):
                corpus = self._getCorpus(corpora, fundingCorpus.id)
                corpusDeduction = min(
                    corpus.getBalance(),
                    recurringAmountToBeDeducted,
                )
                deductions.append({"corpus": corpus, "deduction": corpusDeduction})
                recurringAmountToBeDeducted -= corpusDeduction

        finalCorpus = self._getCorpus(corpora, self.fundingCorpora[-1].id)
        amountToBeDeducted = initialAmountToBeDeducted + recurringAmountToBeDeducted
        print(
            f"Amount to be finally deducted: {amountToBeDeducted.format()} for {self.id} in {year}"
        )
        print(deductions)
        if amountToBeDeducted > finalCorpus.getBalance():
            raise ValueError(
                f"Corpus {finalCorpus.id} doesn't have {amountToBeDeducted} to fund {self.id} in {year}, deductions so far: {deductions}"
            )
            violatedCorpus = finalCorpus

        # deduct any remaining amount from the last corpus, even if it doesn't have enough
        deductions.append({"corpus": finalCorpus, "deduction": amountToBeDeducted})
        return (deductions, violatedCorpus)
