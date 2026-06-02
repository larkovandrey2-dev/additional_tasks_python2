class StrictConfig:
    __slots__ = ("_fields","_values")
    def __init__(self, **kwargs: object) -> None:
        object.__setattr__(self, "_fields", tuple(kwargs.keys()))
        object.__setattr__(self, "_values", dict(kwargs))

    def __setattr__(self, name: str, value: object) -> None:
        if name not in self._values:
            raise AttributeError(f"cannot create new field {name}!r")
        self._values[name] = value
    def __getattr__(self, name: str) -> object:
        values = self._values
        if name in values:
            return values[name]
        raise AttributeError(f"unknown field {name!r}")
    def fields(self) -> tuple[str, ...]:
        return self._fields
    def as_dict(self) -> dict[str, object]:
        return dict(self._values)
    def get(self, name: str) -> object:
        if name not in self._values:
            raise AttributeError(f"unknown field {name!r}")
        return self._values[name]

