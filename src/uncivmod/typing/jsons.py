"""JSON level objects in Unciv."""
from __future__ import annotations

from typing import TYPE_CHECKING, Required, TypedDict

if TYPE_CHECKING:
    from uncivmod.typing import objects


class BeliefJSON(TypedDict, total=False):
    """Beliefs that can be chosen for religions."""

    name: Required[str]
    type: Required[str]
    uniques: list[str]
    civilopediaText: list[objects.CivilopediaText]


class Building(TypedDict):
    """Buildings and wonders."""

    name: Required[str]
    cost: int
    food: int
    production: int
    gold: int
    happiness: int
    culture: int
    science: int
    faith: int
    maintenance: int
    isWonder: bool
    isNationalWonder: bool
    requiredBuilding: str
    cannotBeBuittWith: str
    providesFreeBuilding: str
    requiredTech: str
    requiredResource: str
    requiredNearbylmprovedResources: list[str]
    replaces: str
    uniqueTo: str
    xpForNewUnits: int
    cityStrength: int
    cityHealth: int
    hurryCostModifier: int
    quote: str
    uniques: int
    replacementTextForUniques: list[str]
    percentStatBonus: objects.PercentStats
    greatPersonPoints: dict[str, int]
    civilopediaText: objects.CivilopediaText


class Nation(TypedDict):
    """Nations and city states, including Barbarians and Spectator."""

    name: Required[str]
    leaderName: str
    style: str
    adjective: str
    cityStateType: int
    startBias: list[str]
    preferredVictoryType: objects.VictoryType
    startIntroPart1: str
    startIntroPart2: str
    declaringWar: str
    attacked: str
    defeated: str
    introduction: str
    neutralHeIIo: str
    hateHello: str
    tradeRequest: str
    innerColor: list[int]
    outercolor: list[int]
    uniqueName: int
