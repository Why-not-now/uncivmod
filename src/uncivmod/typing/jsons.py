"""JSON level objects in Unciv."""
from __future__ import annotations

from typing import TYPE_CHECKING, Required, TypedDict

if TYPE_CHECKING:
    from uncivmod.typing import base


class BeliefJSON(TypedDict, total=False):
    """Beliefs that can be chosen for religions."""

    name: Required[str]
    type: Required[base.BeliefEnum]
    uniques: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class BuildingJSON(TypedDict, total=False):
    """Buildings and wonders."""

    name: Required[str]
    cost: int
    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int
    maintenance: int
    isWonder: bool
    isNationalWonder: bool
    requiredBuilding: str
    providesFreeBuilding: str
    requiredTech: str
    requiredResource: str
    requiredNearbyImprovedResources: list[str]
    replaces: str
    uniqueTo: str
    cityStrength: int
    cityHealth: int
    hurryCostModifier: int
    quote: str
    uniques: list[str]
    replacementTextForUniques: str
    percentStatBonus: PercentStatsJSON
    greatPersonPoints: dict[str, int]
    civilopediaText: list[CivilopediaTextJSON]



class CityStateTypeJSON(TypedDict, total=False):
    """Types of city state and its bonuses."""

    name: Required[str]
    color: Required[list[int]]
    friendBonusUniques: list[str]
    allyBonusUniques: list[str]

class DifficultyJSON(TypedDict, total=False):
    """Difficulty levels a player can choose when starting a new game."""

    name: Required[str]
    baseHappiness: int
    extraHappinessPerLuxury: float
    researchCostModifier: float
    unitCostModifier: float
    buildingCostModifier: float
    policyCostModifier: float
    unhappinessModifier: float
    barbarianBonus: float
    playerBonusStartingUnits: list[str]
    aiCityGrowthModifier: float
    aiUnitCostModifier: float
    aiBuildingCostModifier: float
    aiWonderCostModifier: float
    aiBuildingMaintenanceModifier: float
    aiUnitMaintenanceModifier: float
    aiFreeTechs: list[str]
    aiMajorCivBonusStartingUnits: list[str]
    aiCityStateBonusStartingUnits: list[str]
    aiUnhappinessModifier: float
    aisExchangeTechs: bool  # unimplemented
    turnBarbariansCanEnterPlayerTiles: int
    clearBarbarianCampReward: int


class EraJSON(TypedDict, total=False):
    """Eras are usually group technologies together and change gameplay."""

    name: Required[str]
    researchAgreementCost: int
    iconRGB: list[int]
    unitBaseBuyCost: int
    startingSettlerCount: int
    startingSettlerUnit: str
    startingWorkerCount: int
    startingWorkerUnit: str
    startingMilitaryUnitCount: int
    startingMilitaryUnit: str
    startingGold: int
    startingCulture: int
    settlerPopulation: int
    settlerBuildings: list[str]
    startingObsoleteWonders: list[str]
    baseUnitBuyCost: int
    embarkDefense: int
    startPercent: int
    citySound: str


class GlobalUniquesJSON(TypedDict):
    """Defines uniques that apply globally."""

    name: str
    uniques: list[str]


class ImprovementJSON(TypedDict, total=False):
    """Improvements that can be constructed or created on a map tile by a unit."""  # noqa: E501

    name: Required[str]
    terrainsCanBeFoundOn: list[str]
    techRequired: str
    uniqueTo: str
    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int
    turnsToBuild: int
    uniques: list[str]
    shortcutKey: str
    civilopediaText: list[CivilopediaTextJSON]


class ModConstantsJSON(TypedDict, total=False):
    """Collection of constants used internally in Unciv."""

    maxXPfromBarbarians: int
    cityStrengthBase: float
    cityStrengthPerPop: float
    cityStrengthFromTechsMultiplier: float
    cityStrengthFromTechsExponent: float
    cityStrengthFromTechsFullMultipIier: float
    cityStrengthFromGarrison: float
    unitSupplyPerPopulation: float
    minimalCityDistance: int
    minimakCityDistanceOnDifferentContinents: int
    unitUpgradeCost: list[UnitUpgradeCostJSON]
    naturalWonderCountMultiplier: float
    naturalWonderCountAddedConstant: float
    ancientRuinCountMuItipIier: float
    maxLakeSize: int
    riverCountMultiplier: float
    minRiverLength: int
    maxRiverLength: int
    religionLimitBase: int
    religionLimitMultiplier: float
    pantheonBase: int
    pantheonGrowth: int


class ModOptionsJSON(TypedDict, total=False):
    """Metadata and mod-wide options for compatibility."""

    isBaseRuleset: bool
    maxXPfromBarbarians: int  # deprecated
    uniques: list[str]
    techsToRemove: list[str]
    buildingsToRemove: list[str]
    unitsToRemove: list[str]
    nationsToRemove: list[str]
    lastUpdated: str
    modUrl: str
    author: str
    modSize: int
    constants: ModConstantsJSON


class NationJSON(TypedDict, total=False):
    """Nations and city states, including Barbarians and Spectator."""

    name: Required[str]
    leaderName: str
    style: str
    adjective: str  # unused
    cityStateType: str
    startBias: list[str]
    preferredVictoryType: base.VictoryGoalEnum
    startIntroPart1: str
    startIntroPart2: str
    declaringWar: str
    attacked: str
    defeated: str
    introduction: str
    neutralHello: str
    hateHello: str
    tradeRequest: str
    innerColor: list[int]
    outerColor: Required[list[int]]
    uniqueName: str
    uniqueText: str
    uniques: list[str]
    cities: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class PolicyJSON(TypedDict, total=False):
    """Available social policies that can be "bought" with culture."""

    name: Required[str]
    era: Required[str]
    priorities: VictoryPrioritiesJSON
    uniques: list[str]
    policies: list[PolicyMemberJSON]


class PromotionJSON(TypedDict, total=False):
    """Available unit promotions."""

    name: Required[str]
    prerequisites: list[str]
    effect: str  # deprecated
    column: int
    row: int
    unitTypes: list[str]
    uniques: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class QuestJSON(TypedDict, total=False):
    """Quests that may be given to major Civilizations by City States."""

    name: Required[str]
    description: Required[str]
    type: base.QuestEnum
    influence: float
    duration: int
    minimumCivs: int


class ReligionJSON(str):
    """Strings specifying all predefined Religion names."""

    __slots__: tuple[()] = ()


class ResourceJSON(TypedDict, total=False):
    """Resources that a map tile can have."""

    name: Required[str]
    resourceType: base.ResourceEnum
    terrainsCanBeFoundOn: list[str]
    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int
    improvement: str
    improvementStats: StatsJSON
    revealedBy: str
    unique: str
    civilopediaText: list[CivilopediaTextJSON]


class RuinJSON(TypedDict, total=False):
    """Possible rewards ancient ruins give."""

    name: Required[str]
    notification: Required[str]
    weight: int
    uniques: list[str]
    excludedDiffculties: list[str]
    color: base.RGBColour


class SpecialistJSON(TypedDict, total=False):
    """Specialists that populations of a city can be put into."""

    name: Required[str]
    food: int
    production: int
    gold: int
    culture: int
    science: int
    faith: int
    color: Required[list[int]]
    greatPersonPoints: dict[str, int]


class SpeedJSON(TypedDict, total=False):
    """Speeds that determine modifiers to adjust the expected number of rounds in a game of Unciv."""  # noqa: E501

    name: Required[str]
    modifier: float
    productionCostModifier: float
    goldCostModifier: float
    scienceCostModifier: float
    cultureCostModifier: float
    faithCostModifier: float
    improvementBuildLengthModifier: float
    barbarianModifier: float
    goldGiftModifier: float
    cityStateTributeScalingInterval: float
    goldenAgeLengthModifier: float
    religiousPressureAdjacentCity: int
    peaceDealDuration: int
    dealDuration: int
    startYear: float
    turns: Required[list[TimePerTurnJSON]]


class TechColumnJSON(TypedDict):
    """Columns of technologies shown in the technology tree."""

    columnNumber: int
    era: str
    techCost: int
    buildingCost: int
    wonderCost: int
    techs: list[TechJSON]


class TechJSON(TypedDict, total=False):
    """Technologies that can be researched with science."""

    name: Required[str]
    cost: int
    row: int
    prerequisites: list[str]
    quote: str
    uniques: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class TerrainJSON(TypedDict, total=False):
    """Base terrains, terrain features and natural wonders that can appear on the map."""  # noqa: E501

    name: Required[str]
    type: Required[base.TerrainEnum]
    occursOn: list[str]
    turnsInto: str
    weight: int
    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int
    overrideStats: bool
    unbuildable: bool
    impassable: bool
    movementCost: int
    defenceBonus: float
    RGB: list[int]
    uniques: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class TilesetJSON(TypedDict, total=False):
    """Tilesets used in game."""

    useColorAsBaseTerrain: bool
    useSummaryImages: bool
    unexploredTileColor: ColourTilesetJSON
    fogOfWarColor: ColourTilesetJSON
    fallbackTileSet: str | None
    tileScale: float
    tileScales: dict[str, float]
    ruleVariants: dict[str, list[str]]


class TutorialJSON(TypedDict, total=True):
    """Tutorials used in game.

    Note a Base Ruleset mod can define a `welcome page` here by adding a `Tutorial` with a name equal to the name of the mod.
    """  # noqa: E501

    name: Required[str]
    steps: list[str]
    civilopediaText: list[CivilopediaTextJSON]


class UnitJSON(TypedDict, total=False):
    """Units, both military and civilian."""

    name: Required[str]
    unitType: Required[str]
    cost: int
    movement: int
    strength: int
    rangedStrength: int
    range: int
    interceptRange: int
    requiredTech: str
    obsoleteTech: str
    requiredResource: str
    upgradesTo: str
    replaces: str
    uniqueTo: str
    hurryCostModifier: int
    promotions: list[str]
    uniques: list[str]
    replacementTextForUniques: str
    attackSound: str
    civilopediaText: list[CivilopediaTextJSON]


class UnitTypeJSON(TypedDict, total=False):
    """Units, both military and civilian."""

    name: Required[str]
    movementType: Required[base.MovementEnum]
    uniques: list[str]


class UnitUpgradeCostJSON(TypedDict, total=False):
    """Determines the gold cost for a unit to upgrade.

    The formula for the gold cost is (rounded down to a multiple of roundTo):
        (`C`*max((`B`+`P̂`(`Pₜ`-`Pᵢ`)), 0) (1+`N k`))^`E`.

    * `B` being `base`
    * `P̂` being `perProduction`
    * `Pₜ - Pᵢ` being difference in production cost in unit
    * `N` being number of eras that has past
    * `k` being `eraMultiplier`
    * `E` being `exponent`
    * `C` being the multiplicative aggregate of `[relativeAmount]% Gold cost of upgrading` uniques that apply
    """  # noqa: E501

    base: float
    perproduction: float
    eraMultiplier: float
    exponent: float
    roundTo: int


class VictoryType(TypedDict, total=False):
    """Types of victories and requirements for winning."""

    name: Required[str]
    victoryScreenHeader: str
    victoryString: str
    defeatString: str
    hiddenInVictoryScreen: bool
    requiredSpaceshipParts: list[str]
    Milestones: list[str]


class PolicyMemberJSON(TypedDict, total=False):
    """Members of policy."""

    name: Required[str]
    row: Required[int]
    column: Required[int]
    requires: list[str]
    uniques: list[str]


class CivilopediaTextJSON(TypedDict, total=False):
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


class ColourTilesetJSON(TypedDict):  # yes British spelling
    """Colour used for tilesets."""

    r: int
    g: int
    b: int
    a: int


class PercentStatsJSON(TypedDict, total=False):
    """Combinations of percentual stats in base Unciv."""

    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int


class StatsJSON(TypedDict, total=False):
    """Combinations of stats in base Unciv."""

    # until floats are supported, these variables will be integer types
    food: int
    production: int
    gold: int
    science: int
    culture: int
    happiness: int
    faith: int


class TimePerTurnJSON(TypedDict):
    """The amount of time passed between turns and the range of turn numbers that this duration applies to."""  # noqa: E501

    yearsPerTurn: int
    untilTurn: int


class VictoryPrioritiesJSON(TypedDict, total=False):
    """Policy branch's priorities for each victory type."""

    Neutral: int
    Cultural: int
    Diplomatic: int
    Domination: int
    Scientific: int
