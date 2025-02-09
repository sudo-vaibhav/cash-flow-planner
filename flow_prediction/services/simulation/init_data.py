from typing import List, TypedDict

from flow_prediction.aggregates import Expense, Cashflow, Corpus
from flow_prediction.shared.value_objects import Id, Decimal


class Simulation(TypedDict):
    startYear: int
    endYear: int


class CashflowSimulationServiceInitData(TypedDict):
    expenses: List[Expense]
    corpora: List[Corpus]
    cashflows: List[Cashflow]
    simulation: Simulation
    currency: str
    fallbackCorpusId: Id
    baseInflation: Decimal
