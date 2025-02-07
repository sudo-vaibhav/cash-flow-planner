from typing import Optional, TypedDict, List, Union


class AmountReference(TypedDict):
    amount: int
    referenceTime: int


class FundingCorpus(TypedDict):
    id: str


class Expense(TypedDict):
    id: str
    startYear: int
    endYear: int
    enabled: bool
    growthRate: float
    initialValue: AmountReference
    recurringValue: AmountReference
    fundingCorpora: List[FundingCorpus]


class Corpus(TypedDict):
    id: str
    growthRate: float
    startYear: int
    endYear: int
    initialAmount: int
    successorCorpusId: Union[str,None]


class CashflowRecurringValue(TypedDict):
    amount: int
    referenceTime: int
    growthRate: float


class Split(TypedDict):
    corpusId: str
    ratio: float


class Allocation(TypedDict):
    startYear: int
    endYear: int
    split: List[Split]


class Cashflow(TypedDict):
    id: str
    recurringValue: CashflowRecurringValue
    enabled: bool
    startYear: int
    endYear: int
    allocations: List[Allocation]
    expandedDescription: str


class Simulation(TypedDict):
    startYear: int
    endYear: int


class CashflowSimulationUseCaseInitData(TypedDict):
    expenses: List[Expense]
    corpora: List[Corpus]
    cashflows: List[Cashflow]
    simulation: Simulation
    currency: str
