from typing import Sequence, TypedDict

from flow_prediction.shared.value_objects import Id, Decimal


class AllocationSplit(TypedDict):
    corpusId: Id
    ratio: Decimal


class AllocationInitData(TypedDict):
    startYear: int
    endYear: int
    split: Sequence[AllocationSplit]


class Allocation:
    def __init__(self, data: AllocationInitData):
        self.startYear = data["startYear"]
        self.endYear = data["endYear"]
        self.split = data["split"]
        self.validate()

    def overlaps(self, other):
        return self.startYear <= other.endYear and other.startYear <= self.endYear

    def validate(self):
        # split should sum to 1
        allocationSum = sum([split["ratio"] for split in self.split])
        if not allocationSum.isQuantizedEqual(Decimal(1)):
            sumBetween = ",".join([split["corpusId"] for split in self.split])
            raise ValueError(
                f"Allocation split between {sumBetween} should sum to 1, current: "
                + str(allocationSum)
            )

    # def allocate(self):
    #     pass
