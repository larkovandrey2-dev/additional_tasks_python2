class ValidationError(ValueError):
    pass

class Field:
    def __init__(self, expected_type: type, *, min_value: object | None = None) -> None:
        self.expected_type = expected_type
        self.min_value = min_value
        self.name = ""
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object | None, owner: type) -> object:
        if instance is None:
            return self
        return instance.__dict__[self.name]
    def __set__(self, instance: object, value: object) -> None:
        if not isinstance(value, self.expected_type):
            raise ValidationError(f"{self.name} has wrong type")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"{self.name} is too small")
        instance.__dict__[self.name] = value

class ValidatedRecord:
    def __init__(self, **kwargs: object) -> None:
        fields = self._fields()
        for name in kwargs:
            if name not in fields:
                raise TypeError(f"unknown field {name!r}")
        for name in fields:
            if name not in kwargs:
                raise TypeError(f"missing field {name!r}")
            setattr(self, name, kwargs[name])
    def to_dict(self) -> dict[str, object]:
        return {name: getattr(self, name) for name in self._fields()}

    @classmethod
    def schema(cls) -> dict[str, object]:
        result: dict[str, object] = {}
        for name, field in cls._fields().items():
            info: dict[str, object] = {"type": field.expected_type.__name__}
            if field.min_value is not None:
                info["min_value"] = field.min_value
            result[name] = info
        return result

    @classmethod
    def _fields(cls) -> dict[str, Field]:
        result: dict[str, Field] = {}
        for parent in reversed(cls.__mro__):
            for name, value in parent.__dict__.items():
                if isinstance(value, Field):
                    result[name] = value
        return result
