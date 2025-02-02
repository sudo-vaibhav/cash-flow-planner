from abc import ABC
from flow_prediction.shared.value_objects.id import Id


class Aggregate(ABC):
    def __init__(self, id: Id):
        self.id = id

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Aggregate):
            return NotImplemented
        return self.id == value.id

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
