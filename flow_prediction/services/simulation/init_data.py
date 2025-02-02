from typing import List, TypedDict

from flow_prediction.aggregates import Expense, Cashflow, Corpus


class Simulation(TypedDict):
    startYear: int
    endYear: int


class CashflowSimulationServiceInitData(TypedDict):
    expenses: List[Expense]
    corpora: List[Corpus]
    cashflows: List[Cashflow]
    simulation: Simulation
    currency: str
