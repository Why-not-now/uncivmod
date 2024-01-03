"""validators."""
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, cast

if TYPE_CHECKING:
    from typing import Any, Callable

    from attr import Attribute, _ValidatorType


class Comparable[T](Protocol):
    def __lt__(self, other: T) -> bool:
        ...

    def __le__(self, other: T) -> bool:
        ...

    def __eq__(self, other: T) -> bool:
        ...

    def __ne__(self, other: T) -> bool:
        ...

    def __ge__(self, other: T) -> bool:
        ...

    def __gt__(self, other: T) -> bool:
        ...


def _pos( # Comparable[T]
    self: Any,  # noqa: ARG001, ANN401
    attribute: Attribute[int] | Attribute[float],
    value: float,
) -> None:
    if value <= 0:
        msg = f"{attribute.name} must be positive."
        raise ValueError(msg)


def _neg(
    self: Any,  # noqa: ARG001, ANN401
    attribute: Attribute[int] | Attribute[float],
    value: float,
) -> None:
    if value >= 0:
        msg = f"{attribute.name} must be negative."
        raise ValueError(msg)


def _zero[T](self: Any, attribute: Attribute[T], value: T) -> None:  # noqa: ANN401, ARG001
    if value != 0:
        msg = f"{attribute.name} must be zero."
        raise ValueError(msg)


def _eq[T](other: T) -> _ValidatorType[T]:
    def _validator(self: Any, attribute: Attribute[T], value: T) -> None:  # noqa: ANN401, ARG001
        if value != other:
            msg = f"{attribute.name} must be equal to {value}."
            raise ValueError(msg)

    return _validator


def _neq[T](other: T) -> _ValidatorType[T]:
    def _validator(self: Any, attribute: Attribute[T], value: T) -> None:  # noqa: ANN401, ARG001
        if value != other:
            msg = f"{attribute.name} must not equal to {value}."
            raise ValueError(msg)

    return _validator


def _validate_or[T](
    *args: Callable[[Any, Attribute[T], T], Any],
    msg: str | None = None,
) -> _ValidatorType[T]:
    def _validator(self: Any, attribute: Attribute[T], value: T) -> None:  # noqa: ANN401
        error_msg = "" if msg is None else msg

        for validator in args:
            try:
                validator(self, attribute, value)
                break
            except ValueError as e:
                if msg is not None:
                    error_msg += f"{e}\n"

        raise ValueError(error_msg)

    return _validator


def _validate_or_var[T](
    *args: Callable[[Any, Attribute[T], T], Any],
    msg_before: str | None = None,
    msg_after: str | None = None,
) -> _ValidatorType[T]:
    def _validator(self: Any, attribute: Attribute[T], value: T) -> None:  # noqa: ANN401
        if not (msg_before or msg_after):
            msg = "_validate_or_var expected at least 1 error message argument, got 0"  # noqa: E501
            raise TypeError(msg)

        for validator in args:
            try:
                validator(self, attribute, value)
                break
            except ValueError:
                pass

        error_msg = f"{'' if msg_before is None else msg_before}{attribute.name}{'' if msg_after is None else msg_after}"  # noqa: E501
        raise ValueError(error_msg)

    return _validator


def _validate_none[T](
    validator: Callable[[Any, Attribute[T], T], Any],
) -> _ValidatorType[T]:
    def _validator(
        self: Any,  # noqa: ANN401
        attribute: Attribute[T] | Attribute[None],
        value: T | None,
    ) -> None:
        if value is not None:
            if TYPE_CHECKING:
                attribute = cast(Attribute[T], attribute)
            try:
                validator(self, attribute, value)
            except ValueError as e:
                msg = f"{e} or {attribute.name} must be None"
                raise ValueError(msg)  # noqa: B904, TRY200

    return _validator


_ge0 = _validate_or_var(_pos, _zero, msg_after=" must not be negative")
_le0 = _validate_or_var(_neg, _zero, msg_after=" must not be positive")
