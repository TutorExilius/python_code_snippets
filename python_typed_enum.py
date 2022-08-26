from enum import Enum, auto
from types import DynamicClassAttribute


class _TypedEnumBase(Enum):
    def __init_subclass__(cls):
        cls._type_value_map = []


class TypedEnum(_TypedEnumBase):
    def __setattr__(self, key, value):
        if value is None:
            return

        if key == "_value_":

            if type(value) != type:
                raise ValueError("Only datatypes are allowed here as enum values.")

            TypedEnum._type_value_map.append((self, value))
            value = auto()

        super().__setattr__(key, value)

    @DynamicClassAttribute
    def value(self):
        """The value of the Enum member."""

        for item in TypedEnum._type_value_map:
            if item[0] == self:
                return item[1]

    @classmethod
    def value_types(cls):
        return "|".join(set(key.value.__name__ for key in cls))


class ExampleType(TypedEnum):
    TYPE_A: int
    TYPE_B: str
