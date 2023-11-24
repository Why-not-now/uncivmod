"""non-JSON level objects in Unciv."""
from __future__ import annotations

from enum import Enum, auto
from typing import TypedDict


class CivilopediaText(TypedDict, total=False):
    """Supplementary extra text listed in Civilopedia."""

    text: str
    link: str
    icon: str
    extraImage: str
    imageSize: float
    header: str
    size: str
    indent: int
    padding: float
    color: str
    separator: bool
    starred: bool
    centered: bool


class Stats(TypedDict, total=False):
    """Combination of stats in base Unciv."""

    food: int
    production: int
    gold:int
    science: int
    culture: int
    happiness: int
    faith: int


class PercentStats(TypedDict, total=False):
    """Combination of percentual stats in base Unciv."""

    food: int
    production: int
    gold:int
    science: int
    culture: int
    happiness: int
    faith: int

class CityStateType(Enum):
    """Type of city states in Unciv."""

    Neutral = auto()
    Cultural = auto()
    Diplomatic = auto()
    Domination = auto()
    Scientific = auto()

class VictoryType(Enum):
    """Type of victories in base Unciv."""

    Neutral = auto()
    Cultural = auto()
    Diplomatic = auto()
    Domination = auto()
    Scientific = auto()
