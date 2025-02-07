from abc import ABC
from typing import List, TypedDict
from flow_prediction.shared.value_objects import Money, Id
from .init_data import CashflowSimulationServiceInitData
from ...aggregates import Corpus


class CorpusSummary(TypedDict):
    value: float
    id: str

class AllocationCorpusResult:
    value: float
    id: str

class AllocationResult(TypedDict):
    corpora: List[AllocationCorpusResult]
    id : str

class SimulationAnnualResult(TypedDict):
    corpora: List[CorpusSummary]
    year: int
    cashflowAllocation: List[AllocationResult]

class SimulationResponse(TypedDict):
    simulation: List[SimulationAnnualResult]
    warnings: List[str]

class Warning(ABC):
    pass

class OvershotCorpusWarning(Warning):
    def __init__(self, expense_id:str,corpus_id: str, year: int):
        self.corpus_id = corpus_id
        self.year = year
        self.expense_id = expense_id
    def __str__(self):
        return f"Corpus {self.corpus_id} has overshot in year {self.year} due to expense {self.expense_id}"


class CashflowSimulationService:
    def __init__(self, data: CashflowSimulationServiceInitData):
        self.expenses = data["expenses"]
        self.corpora = data["corpora"]
        self.cashflows = data["cashflows"]
        self.simulation = data["simulation"]
        self.currency = data["currency"]

    def _getCorpus(self, id: Id):
        for corpus in self.corpora:
            if corpus.id == id:
                return corpus
        return None

    @staticmethod
    def _overshotCorpusWarningAlreadyExists(warnings: List[Warning], corpus: Corpus):
        for warning in warnings:

            if isinstance(warning, OvershotCorpusWarning) and corpus.id == warning.corpus_id:
                    return True
        return False

    def simulate(self) -> SimulationResponse:
        simulationResults : List[SimulationAnnualResult] = []
        warnings:List[Warning] = []
        for year in range(
            self.simulation["startYear"], self.simulation["endYear"] + 1
        ):
            simulationResult = {
                "corpora": [],
                "year": year,
                "cashflowAllocation": []
            }

            # account for appreciation of all corpora
            for corpus in self.corpora:
                corpus.deposit(corpus.getAnnualAppreciation(year))

            # allocate cashflows to corpora for the year
            for cashflow in self.cashflows:

                allocation = cashflow.getAllocation(year)
                if allocation is None:
                    # TODO: Add logging here
                    continue
                cashflowAllocationResult = {
                    "id": cashflow.id.value,
                    "corpora" : []
                }
                for split in allocation.split:
                    corpus = self._getCorpus(split["corpusId"])
                    if corpus is None:
                        raise ValueError(
                            f"Corpus {split['corpusId']} not found for allocation in cashflow {cashflow.id}"
                        )
                    amount = split["ratio"] * cashflow.getAmount(year)
                    cashflowAllocationResult["corpora"].append(
                    {
                            "id": corpus.id.value,
                            "value": float(amount)
                    })
                    # cashflowAllocation[(cashflow.id,corpus.id)] += amount
                    corpus.deposit(amount)
                simulationResult["cashflowAllocation"].append(cashflowAllocationResult)

            # now time for expenses which must deduct from corpora
            for expense in self.expenses:
                deductions, violatedCorpus = expense.getCorporaDeductions(
                    self.corpora, year
                )
                if violatedCorpus is not None:
                    if not CashflowSimulationService._overshotCorpusWarningAlreadyExists(warnings, violatedCorpus):
                        warnings.append(OvershotCorpusWarning(expense.id.value,violatedCorpus.id.value, year))
                for deduction in deductions:
                    deduction["corpus"].withdraw(deduction["deduction"])
            for corpus in self.corpora:
                simulationResult["corpora"].append(
                    {
                        "id": corpus.id.value,
                        "value": float(corpus.getBalance().amount),
                        "year": year,
                    }
                )
            simulationResults.append(simulationResult)
            # move to successor corpus if a particular corpus is ending
            for corpus in self.corpora:
                if corpus.isEnding(year) and corpus.successorCorpusId is not None:
                    successor = self._getCorpus(corpus.successorCorpusId)
                    if successor is None:
                        raise ValueError(
                            f"Successor corpus {corpus.successorCorpusId} not found for corpus {corpus.id}"
                        )
                    corpus.withdraw(corpus.getBalance())
                    successor.deposit(corpus.getBalance())

        return {"simulation": simulationResults, "warnings": list(map(lambda x:str(x),warnings))}
