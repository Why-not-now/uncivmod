"""non-level objects in Unciv."""
from __future__ import annotations

from enum import auto
from typing import Any, cast

from attrs import Factory, define, field, validators

from uncivmod.typing._typing import _StrEnum
from uncivmod.typing._validator import (
    _ge0,
    _pos,
    _validate_none,
    _validate_or_var,
)


class BeliefEnum(_StrEnum):
    """Types of beliefs in Unciv."""

    Pantheon = auto()
    Follower = auto()
    Founder = auto()
    Enhancer = auto()


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


class QuestEnum(_StrEnum):
    """Types of quests in Unciv."""

    Individual = auto()
    Global = auto()


@define
class PolicyMember:
    """Members of policy."""

    name: str
    row: int
    column: int
    requires: list[str] = Factory(list)
    uniques: list[str] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict = {
            "name": self.name,
            "row": self.row,
            "column": self.column,
        }
        if self.requires:
            return_dict["requires"] = self.requires
        if self.uniques:
            return_dict["uniques"] = self.uniques
        return return_dict


@define
class PolicyFinisher:
    """Finisher of policy."""

    name: str
    uniques: list[str] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        if self.uniques:
            return_dict["uniques"] = self.uniques
        return return_dict


@define
class CivilopediaText:
    """Supplementary extra text listed in Civilopedia."""

    text: str | None
    link: str | None
    icon: str | None
    extra_image: str | None
    image_size: float | None
    header: str | None
    size: str | None
    indent: int | None
    padding: float | None
    colour: str | None
    separator: bool | None
    starred: bool | None
    centered: bool | None

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {}
        for key, value in zip(
            (
                "text",
                "link",
                "icon",
                "extraImage",
                "imageSize",
                "header",
                "size",
                "indent",
                "padding",
                "color",
                "separator",
                "starred",
                "centered",
            ),
            (
                self.text,
                self.link,
                self.icon,
                self.extra_image,
                self.image_size,
                self.header,
                self.size,
                self.indent,
                self.padding,
                self.colour,
                self.separator,
                self.starred,
                self.centered,
            ),
        ):
            if value is not None:
                return_dict[key] = value
        return return_dict


@define
class RGBColour:  # yes British spelling
    """RGB Colour used generally."""

    r: int = field(
        kw_only=True,
        validator=_validate_or_var(
            _ge0,
            validators.le(255),
            msg_after=" is not between 0 and 255",
        ),
    )
    g: int = field(
        kw_only=True,
        validator=_validate_or_var(
            _ge0,
            validators.le(255),
            msg_after=" is not between 0 and 255",
        ),
    )
    b: int = field(
        kw_only=True,
        validator=_validate_or_var(
            _ge0,
            validators.le(255),
            msg_after=" is not between 0 and 255",
        ),
    )

    def to_json(self) -> list[int]:
        """Convert to json format."""
        return [self.r, self.g, self.b]


@define
class ColourTileset:  # yes British spelling
    """Colour used for tilesets."""

    r: float = field(kw_only=True)
    g: float = field(kw_only=True)
    b: float = field(kw_only=True)
    a: float = field(kw_only=True)

    def to_json(self) -> dict[str, float]:
        """Convert to json format."""
        return {"r": self.r, "g": self.g, "b": self.b, "a": self.a}


@define
class Stats:
    """Combinations of stats in base Unciv."""

    production: float = 0
    food: float = 0
    gold: float = 0
    science: float = 0
    culture: float = 0
    happiness: float = 0
    faith: float = 0

    def __bool__(self) -> bool:  # noqa: D105
        return (
            self.production
            == self.food
            == self.gold
            == self.science
            == self.culture
            == self.happiness
            == self.faith
            == 0
        )

    def to_json(self) -> dict[str, float]:
        """Convert to json format."""
        return_dict = {}
        for key, value in zip(
            (
                "production",
                "food",
                "gold",
                "science",
                "culture",
                "happiness",
                "faith",
            ),
            (
                self.production,
                self.food,
                self.gold,
                self.science,
                self.culture,
                self.happiness,
                self.faith,
            ),
        ):
            if value != 0:
                return_dict[key] = value
        return return_dict


@define
class TimePerTurn:
    """The amount of time passed between turns and the range of turn numbers that this duration applies to."""  # noqa: E501 | None

    years_per_turn: int
    until_turn: int

    def to_json(self) -> dict[str, int]:
        """Convert to json format."""
        return {
            "yearsPerTurn": self.years_per_turn,
            "untilTurn": self.until_turn,
        }


@define
class Belief:
    """Beliefs that can be chosen for religions."""

    name: str
    type: BeliefEnum  # noqa: A003
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {
            "name": self.name,
            "type": self.type.value,
        }
        if self.uniques:
            return_dict["uniques"] = self.uniques
        if self.civilopedia_text:
            return_dict["civilopediaText"] = [
                x.to_json() for x in self.civilopedia_text
            ]
        return return_dict


@define
class Building:
    """Buildings and wonders."""

    name: str
    cost: int | None = None  # see TechColumn, only if cost is -1 ¯\_(ツ)_/¯
    production: int = 0
    food: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    maintenance: int = field(default=cast(int, 0), validator=_ge0)
    is_wonder: bool = False
    is_national_wonder: bool = False
    required_building: str = ""
    required_tech: str = ""
    required_resource: str = ""
    required_nearby_improved_resources: list[str] = Factory(list)
    replaces: str = ""
    unique_to: str = ""
    city_strength: int = 0
    city_health: int = 0
    hurry_cost_modifier: int = 0
    quote: str = ""
    uniques: list[str] = Factory(list)
    replacement_text_for_uniques: str = ""
    percent_stat_bonus: Stats = Factory(Stats)
    great_person_points: dict[str, int] = Factory(dict)
    specialist_slots: dict[str, int] = Factory(dict)
    civilopedia_text: list[CivilopediaText] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        for key, value, default in zip(
            (
                "production",
                "food",
                "gold",
                "science",
                "culture",
                "happiness",
                "faith",
                "maintenance",
                "isWonder",
                "isNationalWonder",
                "requiredBuilding",
                "requiredTech",
                "requiredResource",
                "replaces",
                "uniqueTo",
                "cityStrength",
                "cityHealth",
                "hurryCostModifier",
                "quote",
                "replacementTextForUniques",
            ),
            (
                self.production,
                self.food,
                self.gold,
                self.science,
                self.culture,
                self.happiness,
                self.faith,
                self.maintenance,
                self.is_wonder,
                self.is_national_wonder,
                self.required_building,
                self.required_tech,
                self.required_resource,
                self.replaces,
                self.unique_to,
                self.city_strength,
                self.city_health,
                self.hurry_cost_modifier,
                self.quote,
                self.replacement_text_for_uniques,
            ),
            (
                0,  # production
                0,  # food
                0,  # gold
                0,  # science
                0,  # culture
                0,  # happiness
                0,  # faith
                0,  # maintenance
                False,  # is_wonder
                False,  # is_national_wonder
                "",  # required_building
                "",  # required_tech
                "",  # required_resource
                "",  # replaces
                "",  # unique_to
                0,  # city_strength
                0,  # city_health
                0,  # hurry_cost_modifier
                "",  # quote
                "",  # replacement_text_for_uniques
            ),
        ):
            if value != default:
                return_dict[key] = value
        if self.cost is not None:
            return_dict["cost"] = self.cost
        for key, value, default in zip(
            (
                "production",
                "food",
                "gold",
                "science",
                "culture",
                "happiness",
                "faith",
                "maintenance",
                "isWonder",
                "isNationalWonder",
                "requiredBuilding",
                "requiredTech",
                "requiredResource",
                "replaces",
                "uniqueTo",
                "cityStrength",
                "cityHealth",
                "hurryCostModifier",
                "quote",
                "replacementTextForUniques",
            ),
            (
                self.production,
                self.food,
                self.gold,
                self.science,
                self.culture,
                self.happiness,
                self.faith,
                self.maintenance,
                self.is_wonder,
                self.is_national_wonder,
                self.required_building,
                self.required_tech,
                self.required_resource,
                self.replaces,
                self.unique_to,
                self.city_strength,
                self.city_health,
                self.hurry_cost_modifier,
                self.quote,
                self.replacement_text_for_uniques,
            ),
            (
                0,  # production
                0,  # food
                0,  # gold
                0,  # science
                0,  # culture
                0,  # happiness
                0,  # faith
                0,  # maintenance
                False,  # is_wonder
                False,  # is_national_wonder
                "",  # required_building
                "",  # required_tech
                "",  # required_resource
                "",  # replaces
                "",  # unique_to
                0,  # city_strength
                0,  # city_health
                0,  # hurry_cost_modifier
                "",  # quote
                "",  # replacement_text_for_uniques
            ),
        ):
            if value != default:
                return_dict[key] = value
        for key, value in zip(
            (
                "requiredNearbyImprovedResources",
                "uniques",
                "greatPersonPoints",
                "specialistSlots",
            ),
            (
                self.required_nearby_improved_resources,
                self.uniques,
                self.great_person_points,
                self.specialist_slots,
            ),
        ):
            if value:
                return_dict[key] = value
        if self.percent_stat_bonus:
            return_dict["percentStatBonus"] = self.percent_stat_bonus.to_json()
        if self.civilopedia_text:
            return_dict["civilopediaText"] = [
                x.to_json() for x in self.civilopedia_text
            ]
        return return_dict


@define
class CityStateType:
    """City states."""

    name: str
    friend_bonus_uniques: list[str] = Factory(list)
    ally_bonus_uniques: list[str] = Factory(list)
    colour: RGBColour = Factory(lambda: RGBColour(r=255, g=255, b=255))

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        if self.friend_bonus_uniques:
            return_dict["friendBonusUniques"] = self.friend_bonus_uniques
        if self.ally_bonus_uniques:
            return_dict["allyBonusUniques"] = self.ally_bonus_uniques
        if self.colour != RGBColour(r=255, g=255, b=255):
            return_dict["color"] = self.colour
        return return_dict


@define
class Difficulty:
    """Difficulty levels a player can choose when starting a new game."""

    name: str
    base_happiness: int = 0
    extra_happiness_per_luxury: float = 0
    research_cost_modifier: float = 1
    unit_cost_modifier: float = 1
    unit_supply_base: int = 5
    unit_supply_per_city: int = 2
    building_cost_modifier: float = 1
    policy_cost_modifier: float = 1
    unhappiness_modifier: float = 1
    barbarian_bonus: float = 0
    barbarian_spawn_delay: int = 0
    player_bonus_starting_units: list[str] = Factory(list)
    ai_city_growth_modifier: float = 1
    ai_unit_cost_modifier: float = 1
    ai_building_cost_modifier: float = 1
    ai_wonder_cost_modifier: float = 1
    ai_building_maintenance_modifier: float = 1
    ai_unit_maintenance_modifier: float = 1
    ai_unit_supply_modifier: int = 5
    ai_free_techs: list[str] = Factory(list)
    ai_major_civ_bonus_starting_units: list[str] = Factory(list)
    ai_city_state_bonus_starting_units: list[str] = Factory(list)
    ai_unhappiness_modifier: float = 1
    # ais_exchange_techs: bool  # unimplemented  # noqa: ERA001
    turn_barbarians_can_enter_player_tiles: int = 0
    clear_barbarian_camp_reward: int = 25

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        for key, value, default in zip(
            (
                "baseHappiness",
                "extraHappinessPerLuxury",
                "researchCostModifier",
                "unitCostModifier",
                "unitSupplyBase",
                "unitSupplyPerCity",
                "buildingCostModifier",
                "policyCostModifier",
                "unhappinessModifier",
                "barbarianBonus",
                "barbarianSpawnDelay",
                "aiCityGrowthModifier",
                "aiUnitCostModifier",
                "aiBuildingCostModifier",
                "aiWonderCostModifier",
                "aiBuildingMaintenanceModifier",
                "aiUnitMaintenanceModifier",
                "aiUnitSupplyModifier",
                "aiUnhappinessModifier",
                "turnBarbariansCanEnterPlayerTiles",
                "clearBarbarianCampReward",
            ),
            (
                self.base_happiness,
                self.extra_happiness_per_luxury,
                self.research_cost_modifier,
                self.unit_cost_modifier,
                self.unit_supply_base,
                self.unit_supply_per_city,
                self.building_cost_modifier,
                self.policy_cost_modifier,
                self.unhappiness_modifier,
                self.barbarian_bonus,
                self.barbarian_spawn_delay,
                self.ai_city_growth_modifier,
                self.ai_unit_cost_modifier,
                self.ai_building_cost_modifier,
                self.ai_wonder_cost_modifier,
                self.ai_building_maintenance_modifier,
                self.ai_unit_maintenance_modifier,
                self.ai_unit_supply_modifier,
                self.ai_unhappiness_modifier,
                self.turn_barbarians_can_enter_player_tiles,
                self.clear_barbarian_camp_reward,
            ),
            (
                0,  # base_happiness
                0,  # extra_happiness_per_luxury
                1,  # research_cost_modifier
                1,  # unit_cost_modifier
                5,  # unit_supply_base
                2,  # unit_supply_per_city
                1,  # building_cost_modifier
                1,  # policy_cost_modifier
                1,  # unhappiness_modifier
                0,  # barbarian_bonus
                0,  # barbarian_spawn_delay
                1,  # ai_city_growth_modifier
                1,  # ai_unit_cost_modifier
                1,  # ai_building_cost_modifier
                1,  # ai_wonder_cost_modifier
                1,  # ai_building_maintenance_modifier
                1,  # ai_unit_maintenance_modifier
                5,  # ai_unit_supply_modifier
                1,  # ai_unhappiness_modifier
                0,  # turn_barbarians_can_enter_player_tiles
                25,  # clear_barbarian_camp_reward
            ),
        ):
            if value != default:
                return_dict[key] = value
        for key, value in zip(
            (
                "playerBonusStartingUnits",
                "aiFreeTechs",
                "aiMajorCivBonusStartingUnits",
                "aiCityStateBonusStartingUnits",
            ),
            (
                self.player_bonus_starting_units,
                self.ai_free_techs,
                self.ai_major_civ_bonus_starting_units,
                self.ai_city_state_bonus_starting_units,
            ),
        ):
            if value:
                return_dict[key] = value
        return return_dict


@define
class Era:
    """Eras are usually group technologies together and change gameplay."""

    name: str
    research_agreement_cost: int = field(
        default=cast(int, 300),
        validator=_ge0,
    )
    icon_rgb: RGBColour = Factory(lambda: RGBColour(r=255, g=255, b=255))
    starting_settler_count: int = field(default=cast(int, 1), validator=_ge0)
    starting_settler_unit: str = "Settler"
    starting_worker_count: int = field(default=cast(int, 0), validator=_ge0)
    starting_worker_unit: str = "Worker"
    starting_military_unit_count: int = field(
        default=cast(int, 0),
        validator=_ge0,
    )
    starting_military_unit: str = "Warrior"
    starting_gold: int = field(default=cast(int, 0), validator=_ge0)
    starting_culture: int = field(default=cast(int, 0), validator=_ge0)
    settler_population: int = field(default=cast(int, 1), validator=_pos)
    settler_buildings: list[str] = Factory(list)
    starting_obsolete_wonders: list[str] = Factory(list)
    base_unit_buy_cost: int = 200
    embark_defense: int = 3
    start_percent: int = 0
    city_sound: str = "cityClassical"

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        for key, value, default in zip(
            (
                "researchAgreementCost",
                "startingSettlerCount",
                "startingSettlerUnit",
                "startingWorkerCount",
                "startingWorkerUnit",
                "startingMilitaryUnitCount",
                "startingMilitaryUnit",
                "startingGold",
                "startingCulture",
                "settlerPopulation",
                "baseUnitBuyCost",
                "embarkDefense",
                "startPercent",
                "citySound",
            ),
            (
                self.research_agreement_cost,
                self.starting_settler_count,
                self.starting_settler_unit,
                self.starting_worker_count,
                self.starting_worker_unit,
                self.starting_military_unit_count,
                self.starting_military_unit,
                self.starting_gold,
                self.starting_culture,
                self.settler_population,
                self.base_unit_buy_cost,
                self.embark_defense,
                self.start_percent,
                self.city_sound,
            ),
            (
                200,  # research_agreement_cost
                1,  # starting_settler_count
                "Settler",  # starting_settler_unit
                0,  # starting_worker_count
                "Worker",  # starting_worker_unit
                0,  # starting_military_unit_count
                "Warrior",  # starting_military_unit
                0,  # starting_gold
                0,  # starting_culture
                1,  # settler_population
                200,  # base_unit_buy_cost
                3,  # embark_defense
                0,  # start_percent
                "cityClassical",  # city_sound
            ),
        ):
            if value != default:
                return_dict[key] = value
        if self.icon_rgb != RGBColour(r=255, g=255, b=255):
            return_dict["iconRGB"] = self.icon_rgb.to_json()
        if self.settler_buildings:
            return_dict["settlerBuildings"] = self.settler_buildings
        if self.starting_obsolete_wonders:
            return_dict[
                "startingObsoleteWonders"
            ] = self.starting_obsolete_wonders
        return return_dict


@define
class GlobalUniques:
    """Defines uniques that apply globally."""

    name: str | None
    uniques: list[str] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        if self.uniques:
            return_dict["uniques"] = self.uniques
        return return_dict


@define
class Improvement:
    """Improvements that can be constructed or created on a map tile by a unit."""  # noqa: E501 | None

    name: str
    terrains_can_be_found_on: list[str] = Factory(list)
    tech_required: str = ""
    unique_to: str = ""
    production: int = 0
    food: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    turns_to_build: int | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )  # Can not be built if cost is -1 ¯\_(ツ)_/¯, negative same as 0 (always 1 turn)  # noqa: E501
    uniques: list[str] = Factory(list)
    shortcut_key: str = field(
        default=cast(str, ""),
        validator=validators.max_len(1),
    )
    civilopedia_text: list[CivilopediaText] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        for key, value, default in zip(
            (
                "techRequired",
                "uniqueTo",
                "production",
                "food",
                "gold",
                "science",
                "culture",
                "happiness",
                "faith",
                "shortcut_key",
            ),
            (
                self.tech_required,
                self.unique_to,
                self.production,
                self.food,
                self.gold,
                self.science,
                self.culture,
                self.happiness,
                self.faith,
                self.shortcut_key,
            ),
            (
                "",  # tech_required
                "",  # unique_to
                0,  # production
                0,  # food
                0,  # gold
                0,  # science
                0,  # culture
                0,  # happiness
                0,  # faith
                "",  # shortcut_key
            ),
        ):
            if value != default:
                return_dict[key] = value
        if self.turns_to_build is not None:
            return_dict["turnsToBuild"] = self.turns_to_build
        if self.terrains_can_be_found_on:
            return_dict["terrainsCanBeFoundOn"] = self.terrains_can_be_found_on
        if self.uniques:
            return_dict["uniques"] = self.uniques
        if self.civilopedia_text:
            return_dict["civilopediaText"] = [
                x.to_json() for x in self.civilopedia_text
            ]
        return return_dict


@define
class UnitUpgradeCost:
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
    """  # noqa: E501 | None

    base: float = 10
    perproduction: float = 2
    era_multiplier: float = 0
    exponent: float = 1
    round_to: int = 5

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {}
        for key, value, default in zip(
            (
                "base",
                "perproduction",
                "eraMultiplier",
                "exponent",
                "roundTo",
            ),
            (
                self.base,
                self.perproduction,
                self.era_multiplier,
                self.exponent,
                self.round_to,
            ),
            (
                10,  # base
                2,  # perproduction
                0,  # era_multiplier
                1,  # exponent
                5,  # round_to
            ),
        ):
            if value != default:
                return_dict[key] = value
        return return_dict


@define
class ModConstants:
    """Collection of constants used internally in Unciv."""

    max_xp_from_barbarians: int = 30
    city_strength_base: float = 8
    city_strength_per_pop: float = 0.4
    city_strength_from_techs_multiplier: float = 5.5
    city_strength_from_techs_exponent: float = 2.8
    city_strength_from_techs_full_multiplier: float = 1.0
    city_strength_from_garrison: float = 0.2
    unit_supply_per_population: float = 0.5
    minimal_city_distance: int = 3
    minimal_city_distance_on_different_continents: int = 2
    unit_upgrade_cost: UnitUpgradeCost = Factory(UnitUpgradeCost)
    natural_wonder_count_multiplier: float = 0.124
    natural_wonder_count_added_constant: float = 0.1
    ancient_ruin_count_multiplier: float = 0.02
    spawn_ice_below_temperature: float = -0.8
    max_lake_size: int = 10
    river_count_multiplier: float = 0.01
    min_river_length: int = 5
    max_river_length: int = 666  # 😈😈😈
    religion_limit_base: int = 1
    religion_limit_multiplier: float = 0.5
    pantheon_base: int = 10
    pantheon_growth: int = 5

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {}
        for key, value, default in zip(
            (
                "maxXPFromBarbarians",
                "cityStrengthBase",
                "cityStrengthPerPop",
                "cityStrengthFromTechsMultiplier",
                "cityStrengthFromTechsExponent",
                "cityStrengthFromTechsFullMultiplier",
                "cityStrengthFromGarrison",
                "unitSupplyPerPopulation",
                "minimalCityDistance",
                "minimalCityDistanceOnDifferentContinents",
                "naturalWonderCountMultiplier",
                "naturalWonderCountAddedConstant",
                "ancientRuinCountMultiplier",
                "spawnIceBelowTemperature",
                "maxLakeSize",
                "riverCountMultiplier",
                "minRiverLength",
                "maxRiverLength",
                "religionLimitBase",
                "religionLimitMultiplier",
                "pantheonBase",
                "pantheonGrowth",
            ),
            (
                self.max_xp_from_barbarians,
                self.city_strength_base,
                self.city_strength_per_pop,
                self.city_strength_from_techs_multiplier,
                self.city_strength_from_techs_exponent,
                self.city_strength_from_techs_full_multiplier,
                self.city_strength_from_garrison,
                self.unit_supply_per_population,
                self.minimal_city_distance,
                self.minimal_city_distance_on_different_continents,
                self.natural_wonder_count_multiplier,
                self.natural_wonder_count_added_constant,
                self.ancient_ruin_count_multiplier,
                self.spawn_ice_below_temperature,
                self.max_lake_size,
                self.river_count_multiplier,
                self.min_river_length,
                self.max_river_length,
                self.religion_limit_base,
                self.religion_limit_multiplier,
                self.pantheon_base,
                self.pantheon_growth,
            ),
            (
                30,  # max_xp_from_barbarians
                8,  # city_strength_base
                0.4,  # city_strength_per_pop
                5.5,  # city_strength_from_techs_multiplier
                2.8,  # city_strength_from_techs_exponent
                1.0,  # city_strength_from_techs_full_multiplier
                0.2,  # city_strength_from_garrison
                0.5,  # unit_supply_per_population
                3,  # minimal_city_distance
                2,  # minimal_city_distance_on_different_continents
                0.1,  # natural_wonder_count_multiplier
                0.1,  # natural_wonder_count_added_constant
                0.02,  # ancient_ruin_count_multiplier
                -0.8,  # spawn_ice_below_temperature
                10,  # max_lake_size
                0.0,  # river_count_multiplier
                5,  # min_river_length
                666,  # max_river_length
                1,  # religion_limit_base
                0.5,  # religion_limit_multiplier
                10,  # pantheon_base
                5,  # pantheon_growth
            ),
        ):
            if value != default:
                return_dict[key] = value
        unit_upgrade_cost_json = self.unit_upgrade_cost.to_json()
        if unit_upgrade_cost_json:
            return_dict["unitUpgradeCost"] = unit_upgrade_cost_json
        return return_dict


@define
class ModOptions:
    """Metadata and mod-wide options for compatibility."""

    is_base_ruleset: bool = False
    uniques: list[str] = Factory(list)
    techs_to_remove: list[str] = Factory(list)
    buildings_to_remove: list[str] = Factory(list)
    units_to_remove: list[str] = Factory(list)
    nations_to_remove: list[str] = Factory(list)
    constants: ModConstants = Factory(ModConstants)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {}
        if self.is_base_ruleset:
            return_dict["isBaseRuleset"] = self.is_base_ruleset
        for key, value in zip(
            (
                "uniques",
                "techsToRemove",
                "buildingsToRemove",
                "unitsToRemove",
                "nationsToRemove",
            ),
            (
                self.uniques,
                self.techs_to_remove,
                self.buildings_to_remove,
                self.units_to_remove,
                self.nations_to_remove,
            ),
        ):
            if value:
                return_dict[key] = value
        constants_json = self.constants.to_json()
        if constants_json:
            return_dict["unitUpgradeCost"] = constants_json
        return return_dict


@define
class Nation:
    """Nations and city states, including Barbarians and Spectator."""

    name: str
    outer_colour: RGBColour
    leader_name: str = ""
    style: str = ""
    city_state_type: str = ""
    # adjective: str = ""   TODO
    start_bias: list[str] = Factory(list)
    preferred_victory_type: str = "Neutral"
    favoured_religion: str = ""
    start_intro_part1: str = ""
    start_intro_part2: str = ""
    declaring_war: str = ""
    attacked: str = ""
    defeated: str = ""
    introduction: str = ""
    neutral_hello: str = ""
    hate_hello: str = ""
    trade_request: str = ""
    inner_colour: RGBColour = Factory(lambda: RGBColour(r=0, g=0, b=0))
    unique_name: str = ""
    unique_text: str = ""
    uniques: list[str] = Factory(list)
    cities: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {
            "name": self.name,
            "outerColor": self.outer_colour,
        }
        for key, value, default in zip(
            (
                "leaderName",
                "style",
                "cityStateType",
                "startBias",
                "preferredVictoryType",
                "favouredReligion",
                "startIntroPart1",
                "startIntroPart2",
                "declaringWar",
                "attacked",
                "defeated",
                "introduction",
                "neutralHello",
                "hateHello",
                "tradeRequest",
                "innerColor",
                "uniqueName",
                "uniqueText",
            ),
            (
                self.leader_name,
                self.style,
                self.city_state_type,
                self.start_bias,
                self.preferred_victory_type,
                self.favoured_religion,
                self.start_intro_part1,
                self.start_intro_part2,
                self.declaring_war,
                self.attacked,
                self.defeated,
                self.introduction,
                self.neutral_hello,
                self.hate_hello,
                self.trade_request,
                self.inner_colour,
                self.unique_name,
                self.unique_text,
            ),
            (
                "",
                "",
                "",
                "Neutral",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ),
        ):
            if value != default:
                return_dict[key] = value
        for key, value in zip(
            (
                "startBias",
                "uniques",
                "cities",
            ),
            (
                self.start_bias,
                self.uniques,
                self.cities,
            ),
        ):
            if value:
                return_dict[key] = value
        if self.civilopedia_text:
            return_dict["civilopediaText"] = [
                x.to_json() for x in self.civilopedia_text
            ]
        return return_dict


@define
class Policy:
    """Available social policies that can be "bought" with culture."""

    name: str
    era: str
    priorities: dict[str, int] = Factory(dict)
    uniques: list[str] = Factory(list)
    policies: dict[str, PolicyMember | PolicyFinisher] = Factory(dict)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name, "era": self.era}
        if self.priorities:
            return_dict["priorities"] = self.priorities
        if self.uniques:
            return_dict["uniques"] = self.uniques
        if self.policies:
            return_dict["policies"] = [
                x.to_json() for x in self.policies.values()
            ]
        return return_dict


@define
class Promotion:
    """Available unit promotions."""

    name: str
    prerequisites: list[str] = Factory(list)
    row: int | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    column: int = field(default=cast(int, 0), validator=_ge0)
    unit_types: list[str] = Factory(list)
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {"name": self.name}
        if self.row is not None:
            return_dict["row"] = self.row
        if self.column != 0:
            return_dict["column"] = self.column
        for key, value in zip(
            (
                "prerequisites",
                "unitTypes",
                "uniques",
            ),
            (
                self.prerequisites,
                self.unit_types,
                self.uniques,
            ),
        ):
            if value:
                return_dict[key] = value
        if self.civilopedia_text:
            return_dict["civilopediaText"] = [
                x.to_json() for x in self.civilopedia_text
            ]
        return return_dict


@define
class Quest:
    """Quests that may be given to all major Civilizations by City States."""

    name: str
    description: str
    type: QuestEnum  # noqa: A003
    influence: float = 40
    duration: int = 0
    minimum_civs: int = 1
    weight_for_city_state_type: dict[str, float] = Factory(dict)

    def to_json(self) -> dict[str, Any]:
        """Convert to json format."""
        return_dict: dict[str, Any] = {
            "name": self.name,
            "description": self.description,
        }
        for key, value, default in zip(
            (
                "influence",
                "duration",
                "minimumCivs",
            ),
            (
                self.influence,
                self.duration,
                self.minimum_civs,
            ),
            (
                40,  # influence
                0,  # duration
                1,  # minimum_civs
            ),
        ):
            if value != default:
                return_dict[key] = value
        if self.weight_for_city_state_type:
            return_dict[
                "weightForCityStateType"
            ] = self.weight_for_city_state_type
        return return_dict


class Religion(str):  # must have image
    """Strings specifying all predefined Religion names."""

    __slots__: tuple[()] = ()


@define
class Resource:
    """Resources that a map tile can have."""

    name: str
    resource_type: ResourceEnum = ResourceEnum.Bonus
    terrains_can_be_found_on: list[str] = Factory(list)
    production: int = 0
    food: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    improvement_stats: Stats = Factory(Stats)
    revealed_by: str = ""
    improved_by: list[str] = Factory(list)
    unique: str = ""
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Ruin:
    """Possible rewards ancient ruins give."""

    name: str
    notification: str
    weight: int = field(default=cast(int, 1), validator=_ge0)
    uniques: list[str] = Factory(list)
    excluded_diffculties: list[str] = Factory(list)


@define
class Specialist:
    """Specialists that populations of a city can be put into."""

    name: str
    colour: RGBColour
    production: float = 0
    food: float = 0
    gold: float = 0
    science: float = 0
    culture: float = 0
    happiness: float = 0
    faith: float = 0
    great_person_points: dict[str, int] = Factory(dict)


@define
class Speed:
    """Speeds that determine modifiers to adjust the expected number of rounds in a game of Unciv."""  # noqa: E501 | None

    name: str
    turns: list[TimePerTurn]
    modifier: float = field(default=cast(int, 1), validator=_ge0)
    production_cost_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    gold_cost_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    science_cost_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    culture_cost_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    faith_cost_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    improvement_build_length_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    barbarian_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    gold_gift_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    city_state_tribute_scaling_interval: float = field(
        default=cast(int, 6.5),
        validator=_ge0,
    )
    golden_age_length_modifier: float | None = field(
        default=cast(int | None, None),
        validator=_validate_none(_ge0),
    )
    religious_pressure_adjacent_city: int = field(
        default=cast(int, 6),
        validator=_ge0,
    )
    peace_deal_duration: int = field(
        default=cast(int, 10),
        validator=_ge0,
    )
    deal_duration: int = field(default=cast(int, 30), validator=_ge0)
    start_year: float = -4000


@define
class Tech:
    """Technologies that can be researched with science."""

    name: str
    cost: int = 0  # if 0 get from TechColumn
    row: int = 0
    prerequisites: list[str] = Factory(list)
    quote: str = ""
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class TechColumn:
    """Columns of technologies shown in the technology tree."""

    column_number: int
    era: str
    tech_cost: int
    building_cost: int
    wonder_cost: int
    techs: list[Tech]


class TechTree(list[TechColumn]):
    """Technology tree."""


@define
class Terrain:
    """Terrains that can appear on the map."""

    name: str
    type: TerrainEnum  # noqa: A003
    occurs_on: list[str] = Factory(list)
    turns_into: str = ""
    weight: int = 10
    production: int = 0
    food: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    override_stats: bool = False
    unbuildable: bool = False
    impassable: bool = False
    movement_cost: int = 1
    defence_bonus: float = 0
    rgb: RGBColour = Factory(lambda: RGBColour(r=255, g=215, b=0))
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Tileset:
    """Tilesets used in game."""

    use_colour_as_base_terrain: bool = False
    use_summary_images: bool = False
    unexplored_tile_colour: ColourTileset = Factory(
        lambda: ColourTileset(r=0.25, g=0.25, b=0.25, a=1),
    )
    fog_of_war_colour: ColourTileset = Factory(
        lambda: ColourTileset(r=0, g=0, b=0, a=1),
    )
    fallback_tile_set: str = ""
    tile_scale: float = 1
    tile_scales: dict[str, float] = Factory(dict)
    rule_variants: dict[str, list[str]] = Factory(dict)


@define
class Tutorial:
    """Tutorials used in game.

    Note a Base Ruleset mod can attrs a `welcome page` here by adding a `Tutorial` with a name equal to the name of the mod.
    """  # noqa: E501

    name: str
    steps: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Unit:
    """Units, both military and civilian."""

    name: str
    unit_type: str
    cost: int = -1
    movement: int = field(default=cast(int, 0), validator=_ge0)
    strength: int = 0
    ranged_strength: int = 0
    religious_strength: int = 0
    range: int = field(default=cast(int, 2), validator=_ge0)  # noqa: A003
    intercept_range: int = field(default=cast(int, 0), validator=_ge0)
    required_tech: str = ""
    obsolete_tech: str = ""
    required_resource: str = ""
    upgrades_to: str = ""
    replaces: str = ""
    unique_to: str = ""
    hurry_cost_modifier: int = 0
    promotions: list[str] = Factory(list)
    uniques: list[str] = Factory(list)
    replacement_text_for_uniques: str = ""
    attack_sound: str = ""
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class UnitType:
    """Units, both military and civilian."""

    name: str
    movement_type: MovementEnum
    uniques: list[str] = Factory(list)


@define
class VictoryType:
    """Types of victories and requirements for winning."""

    name: str
    victory_screen_header: str = ""
    victory_string: str = ""
    defeat_string: str = ""
    hidden_in_victory_screen: bool = False
    required_spaceship_parts: list[str] = Factory(list)
    milestones: list[str] = Factory(list)


@define
class UncivMod:
    beliefs: dict[str, Belief] = Factory(dict)
    buildings: dict[str, Building] = Factory(dict)
    difficulties: dict[str, Difficulty] = Factory(dict)
    eras: dict[str, Era] = Factory(dict)
    global_uniques: list[GlobalUniques] = Factory(list)
    improvements: dict[str, Improvement] = Factory(dict)
    mod_constants: ModConstants = Factory(ModConstants)
    nations: dict[str, Nation] = Factory(dict)
    policies: dict[str, Policy] = Factory(dict)
    promotions: dict[str, Promotion] = Factory(dict)
    quests: dict[str, Quest] = Factory(dict)
    religions: list[Religion] = Factory(list)
    resources: dict[str, Resource] = Factory(dict)
    ruins: dict[str, Ruin] = Factory(dict)
    specialists: dict[str, Specialist] = Factory(dict)
    speeds: dict[str, Speed] = Factory(dict)
    techs: TechTree = Factory(TechTree)
    terrains: dict[str, Terrain] = Factory(dict)
    victory_type: dict[str, VictoryType] = Factory(dict)
