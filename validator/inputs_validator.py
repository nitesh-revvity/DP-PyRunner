import enum
from typing import get_origin, get_args, Union, Optional
import inspect
import functools

def _convert_value(value, expected_type):
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    # Handle Optional and Union types
    if origin is Union:
        # None allowed in Optional
        for typ in args:
            try:
                return _convert_value(value, typ)
            except Exception:
                continue
        raise TypeError(f"Value {value!r} does not match any of {args}")

    # None type handling
    if expected_type is type(None):
        if value is None:
            return None
        raise TypeError(f"Expected None, got {type(value).__name__}")

    # Enum handling
    if isinstance(expected_type, type) and issubclass(expected_type, enum.Enum):
        if isinstance(value, expected_type):
            return value
        try:
            return expected_type(value)
        except ValueError:
            raise ValueError(f"Invalid Enum value {value!r} for {expected_type.__name__}")

    # Primitive types
    if expected_type is bool:
        if isinstance(value, str):
            if value.lower() in ("true", "1"): return True
            if value.lower() in ("false", "0"): return False
            raise ValueError(f"Cannot convert string {value!r} to bool")
        return bool(value)

    if expected_type in (int, float, str):
        try:
            return expected_type(value)
        except (ValueError, TypeError):
            raise TypeError(f"Cannot convert {value!r} to {expected_type.__name__}")

    # Already correct type
    if isinstance(value, expected_type):
        return value

    raise TypeError(f"Unsupported or mismatched type for {value!r} -> {expected_type}")


def validate_inputs(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound = sig.bind_partial(*args, **kwargs)
        bound.apply_defaults()

        for name, value in bound.arguments.items():
            expected_type = sig.parameters[name].annotation
            if expected_type is inspect._empty:
                continue  # No type annotation
            try:
                bound.arguments[name] = _convert_value(value, expected_type)
            except Exception as e:
                raise TypeError(
                    f"Invalid type for argument '{name}': "
                    f"expected {expected_type}, got {type(value).__name__} ({e})"
                )

        return await func(*bound.args, **bound.kwargs)
    return wrapper

