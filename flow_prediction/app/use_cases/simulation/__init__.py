from flow_prediction.aggregates import Expense, Corpus, Cashflow
from flow_prediction.aggregates.expense import FundingCorpus
from flow_prediction.services.simulation import CashflowSimulationService
from flow_prediction.shared.value_objects import (
    InflationAdjustableValue,
    Money,
    Decimal,
    Id,
)
from .init_data import CashflowSimulationUseCaseInitData
from .. import UseCase


class CashflowSimulationUseCase(UseCase):
    def __init__(self, data: CashflowSimulationUseCaseInitData):
        self.data = data

    def execute(self):
        corpora = list(
            map(
                lambda d: Corpus(
                    Id(d["id"]),
                    Decimal(d["growthRate"]),
                    Money(d["initialAmount"]),
                    d["startYear"],
                    d["endYear"],
                    (Id(d["successorCorpusId"]) if "successorCorpusId" in d else None),
                ),
                self.data["corpora"],
            )
        )
        return CashflowSimulationService(
            {
                "expenses": list(
                    map(
                        lambda d: Expense(
                            Id(d["id"]),
                            d["startYear"],
                            d["endYear"],
                            d["enabled"],
                            InflationAdjustableValue(
                                amount=Money(d["initialValue"]["amount"]),
                                growthRate=Decimal(d["growthRate"]),
                                referenceTime=d["initialValue"]["referenceTime"],
                            ),
                            InflationAdjustableValue(
                                amount=Money(d["recurringValue"]["amount"]),
                                growthRate=Decimal(d["growthRate"]),
                                referenceTime=d["recurringValue"]["referenceTime"],
                            ),
                            fundingCorpora=(
                                list(
                                    map(
                                        lambda fc: FundingCorpus(
                                            Id(fc["id"]),
                                            fc.get("startYear", None),
                                            fc.get("forInitialOnly", False),
                                        ),
                                        d["fundingCorpora"],
                                    )
                                )
                                if "fundingCorpora" in d
                                else None
                            ),
                            corpora=corpora,
                        ),
                        self.data["expenses"],
                    )
                ),
                "corpora": corpora,
                "cashflows": list(
                    map(
                        lambda d: Cashflow(
                            data={
                                "enabled": d["enabled"],
                                "id": Id(d["id"]),
                                "startYear": d["startYear"],
                                "endYear": d["endYear"],
                                "expandedDescription": d["expandedDescription"],
                                "recurringValue": InflationAdjustableValue(
                                    Money(d["recurringValue"]["amount"]),
                                    d["recurringValue"]["referenceTime"],
                                    Decimal(d["recurringValue"]["growthRate"]),
                                ),
                                "allocations": list(
                                    map(
                                        lambda d2: Cashflow.Allocation(
                                            {
                                                "startYear": d2["startYear"],
                                                "endYear": d2["endYear"],
                                                "split": list(
                                                    map(
                                                        lambda d3: (
                                                            {
                                                                "corpusId": Id(
                                                                    d3["corpusId"]
                                                                ),
                                                                "ratio": Decimal(
                                                                    d3["ratio"]
                                                                ),
                                                            }
                                                        ),
                                                        d2["split"],
                                                    )
                                                ),
                                            }
                                        ),
                                        d["allocations"],
                                    )
                                ),
                            }
                        ),
                        self.data["cashflows"],
                    )
                ),
                "simulation": {
                    "startYear": self.data["simulation"]["startYear"],
                    "endYear": self.data["simulation"]["endYear"],
                },
                "currency": self.data["currency"],
                "fallbackCorpusId": Id(self.data["fallbackCorpusId"]),
                "baseInflation": Decimal(self.data["baseInflation"]),
            }
        ).simulate()


__all__ = ["CashflowSimulationUseCase", "CashflowSimulationUseCaseInitData"]
