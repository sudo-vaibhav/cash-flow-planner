from collections import defaultdict
from typing import Dict, List, TypedDict
from flow_prediction.shared.value_objects import Money, Id
from .init_data import CashflowSimulationServiceInitData


class CorpusSummary(TypedDict):
    value: float
    year: int


class SimulationResponse(TypedDict):
    simulation: Dict[str, List[CorpusSummary]]
    warnings: List[str]


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

    def simulate(self) -> SimulationResponse:
        corporaSimulation: Dict[str, List[CorpusSummary]] = defaultdict(list)
        warnings = []
        for year in range(
            self.simulation["startYear"], self.simulation["endYear"] + 1
        ):

            # account for appreciation of all corpora
            for corpus in self.corpora:
                corpus.deposit(corpus.getAnnualAppreciation(year))

            # allocate cashflows to corpora for the year
            for cashflow in self.cashflows:
                allocation = cashflow.getAllocation(year)
                if allocation is None:
                    # TODO: Add logging here
                    continue
                for split in allocation.split:
                    corpus = self._getCorpus(split["corpusId"])
                    if corpus is None:
                        raise ValueError(
                            f"Corpus {split['corpusId']} not found for allocation in cashflow {cashflow.id}"
                        )
                    amount = split["ratio"] * cashflow.getAmount(year)
                    corpus.deposit(amount)

            # now time for expenses which must deduct from corpora
            for expense in self.expenses:
                deductions, deductionWarnings = expense.getCorporaDeductions(
                    self.corpora, year
                )
                warnings.extend(deductionWarnings)
                for deduction in deductions:
                    deduction["corpus"].withdraw(deduction["deduction"])
            for corpus in self.corpora:
                corporaSimulation[corpus.id.value].append(
                    {
                        "value": float(corpus.getBalance().amount),
                        "year": year,
                    }
                )
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

        return {"simulation": corporaSimulation, "warnings": warnings}
