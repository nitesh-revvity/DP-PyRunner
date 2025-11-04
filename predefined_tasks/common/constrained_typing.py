import inspect
from functools import wraps
from enum import Enum
from typing import get_origin, get_args


def _convert_value_new(value, expected_type):
    if expected_type is bool and isinstance(value, str):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        raise ValueError(f"Invalid boolean string: '{value}'")

    if isinstance(expected_type, type) and issubclass(expected_type, Enum):
        if isinstance(value, expected_type):
            return value
        return expected_type(value)

    if expected_type in [int, float, str] and isinstance(value, str):
        return expected_type(value)

    if expected_type in [Wavelength, VoltagePMT, Percentage] and isinstance(value, int):
        return expected_type(value)

    

    return value

def validate_inputs(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        updated = {}

        for name, param in sig.parameters.items():
            if name not in bound.arguments:
                continue

            value = bound.arguments[name]
            expected_type = param.annotation

            if expected_type is inspect._empty:
                updated[name] = value
                continue

            origin = get_origin(expected_type)

            try:
                if origin is not None:
                    possible_types = get_args(expected_type)

                    enum_types = [t for t in possible_types if isinstance(t, type) and issubclass(t, Enum)]
                    non_enum_types = [t for t in possible_types if t not in enum_types]

                    # Try enums first
                    for enum_type in enum_types:
                        try:
                            converted = _convert_value_new(value, enum_type)
                            if isinstance(converted, enum_type):
                                updated[name] = converted
                                break
                        except Exception:
                            pass
                    else:
                        # Try other types if enums failed
                        for other_type in non_enum_types:
                            try:
                                converted = _convert_value_new(value, other_type)
                                if isinstance(converted, other_type):
                                    updated[name] = converted
                                    break
                            except Exception:
                                continue
                        else:
                            raise TypeError(
                                f"Argument '{name}' expects one of {possible_types}, got {value}"
                            )
                else:
                    converted = _convert_value_new(value, expected_type)
                    if not isinstance(converted, expected_type):
                        raise TypeError(
                            f"Argument '{name}' expects {expected_type.__name__}, got {type(value).__name__}"
                        )
                    updated[name] = converted


            except Exception as e:
                raise TypeError(f"Argument '{name}' validation error: {e}")


        return await func(**updated)

    return wrapper

# Data Types:

    
class PlateType(Enum):
    WellPlate_6 = 6
    WellPlate_12 = 12
    WellPlate_24 = 24
    WellPlate_48 = 48
    WellPlate_96 = 96
    WellPlate_384 = 384

    def __eq__(self, other):
        if isinstance(other, PlateType):
            return self.value == other.value
        if isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __hash__(self):
        return hash(self.value)


class Wavelength(int):
    min_value = 200
    max_value = 1000
    def __new__(cls, value):
        if not (cls.min_value <= value <= cls.max_value):
            raise ValueError(f"Wavelength must be between {cls.min_value} and {cls.max_value}")
        return super().__new__(cls, value)


class VoltagePMT(int):
    max_value = 0.7
    min_value = 0.4
    def __new__(cls, value):
        if not (cls.min_value <= value <= cls.max_value):
            raise ValueError(f"VoltagePMT must be between  {cls.min_value} and {cls.max_value}")
        return super().__new__(cls, value)

class Percentage(int):
    max_value = 0
    min_value = 100
    def __new__(cls, value):
        if not (cls.min_value <= value <= cls.max_value):
            raise ValueError(f"Percentage must be between  {cls.min_value} and {cls.max_value}")
        return super().__new__(cls, value)