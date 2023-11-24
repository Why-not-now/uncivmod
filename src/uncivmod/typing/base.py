"""non-JSON level objects in Unciv."""
from __future__ import annotations

from enum import auto

from uncivmod.typing._typing import _StrEnum


class BeliefEnum(_StrEnum):
    """Types of beliefs in Unciv."""

    Pantheon = auto()
    Follower = auto()
    Founder = auto()
    Enhancer = auto()


class CityStateEnum(_StrEnum):
    """Types of city states in Unciv."""

    Neutral = auto()
    Cultural = auto()
    Diplomatic = auto()
    Domination = auto()
    Scientific = auto()


class MovementEnum(_StrEnum):
    """Types of movements in Unciv."""

    Water = auto()
    Land = auto()
    Air = auto()


class ResourceEnum(_StrEnum):
    """Types of resources in Unciv."""

    Bonus = auto()
    Luxury = auto()
    Strategic = auto()


class TerrainEnum(_StrEnum):
    """Types of terrains in Unciv."""

    Land = auto()
    Water = auto()
    TerrainFeature = auto()
    NaturalWonder = auto()


class VictoryGoalEnum(_StrEnum):
    """Types of victories the AI will try to achieve in base Unciv."""

    Neutral = auto()
    Cultural = auto()
    Diplomatic = auto()
    Domination = auto()
    Scientific = auto()


class QuestEnum(_StrEnum):
    """Types of quests in Unciv."""

    Individual = auto()
    Global = auto()
