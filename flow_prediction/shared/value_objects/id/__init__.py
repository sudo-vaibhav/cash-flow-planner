class Id:
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return str(self._value)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Id):
            return NotImplemented
        return self._value == o._value

    def __repr__(self):
        return f"Id(value={self._value})"
