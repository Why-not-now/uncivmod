"""Handles files in the uncivmod module.

Can read/write json, or entire folders.
"""
from __future__ import annotations

from typing import cast

from attr import Attribute
from attrs import define, field


def _check(self, attribute: Attribute[int], value: int):
    print(type(attribute))
    if value > 42:
        msg = "x must be smaller or equal to 42"
        raise ValueError(msg)


def trick_type_hinter() -> int:
    print(Attribute)
    return 1


@define
class LiteralDefault:
    x: int = field(factory=trick_type_hinter, validator=_check)
