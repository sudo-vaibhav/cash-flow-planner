import pprint

from .data import data
from .use_cases.simulation import CashflowSimulationUseCase


if __name__ == "__main__":

    simulationResult = CashflowSimulationUseCase(data)

    pprint.pprint(simulationResult.execute())
