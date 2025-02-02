from flow_prediction.shared.value_objects import Money, Id
from .init_data import CashflowSimulationServiceInitData


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

    def simulate(self):
        summary = []
        for year in range(
            self.simulation["startYear"], self.simulation["endYear"] + 1
        ):
            # account for appreication of all corpora
            for corpus in self.corpora:
                corpus.deposit(corpus.getAnnualAppreciation())

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
                deductions = expense.getCorporaDeductions(self.corpora, year)
                for deduction in deductions:
                    deduction["corpus"].withdraw(deduction["deduction"])
            summary.append(
                {
                    "year": year,
                    "corpora": [
                        corpus.getBalance().amount for corpus in self.corpora
                    ],
                }
            )
        return summary
