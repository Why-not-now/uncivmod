"""non- level objects in Unciv."""
from __future__ import annotations

from enum import auto
from typing import TYPE_CHECKING, cast

from attrs import Factory, define, field, validators

from uncivmod.typing._typing import _StrEnum

if TYPE_CHECKING:
    from typing import Any, Callable

    from attr import Attribute, _ValidatorType

    from uncivmod.typing import jsons


def _pos(self: Any, attribute: Attribute[int], value: int) -> None:  # noqa: ANN401, ARG001
    if value <= 0:
        msg = f"{attribute.name} must be positive."
        raise ValueError(msg)


def _neg(self: Any, attribute: Attribute[int], value: int) -> None:  # noqa: ANN401, ARG001
    if value >= 0:
        msg = f"{attribute.name} must be negative."
        raise ValueError(msg)


def _zero(self: Any, attribute: Attribute[int], value: int) -> None:  # noqa: ANN401, ARG001
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
    *args: Callable[[Any, Attribute[T], T], Any], msg: str | None = None
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
    validator: Callable[[Any, Attribute[T], T], Any]
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


class BeliefEnum(_StrEnum):
    """Types of beliefs in Unciv."""

    Pantheon = auto()
    Follower = auto()
    Founder = auto()
    Enhancer = auto()


class CityStateEnum(_StrEnum):
    """Types of city states in Unciv."""

    absent = auto()
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
class PolicyMember:
    """Members of policy."""

    name: str
    row: int
    column: int
    requires: list[str] = Factory(list)
    uniques: list[str] = Factory(list)


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


@define
class RGBColour:  # yes British spelling
    """RGB Colour used generally."""

    r: int = field(default=0, kw_only=True)
    g: int = field(default=0, kw_only=True)
    b: int = field(default=0, kw_only=True)


@define
class ColourTileset:  # yes British spelling
    """Colour used for tilesets."""

    r: int = field(default=0, kw_only=True)
    g: int = field(default=0, kw_only=True)
    b: int = field(default=0, kw_only=True)
    a: int = field(default=0, kw_only=True)


@define
class PercentStats:
    """Combinations of percentual stats in base Unciv."""

    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0


@define
class Stats:
    """Combinations of stats in base Unciv."""

    # until floats are supported, these variables will be integer types
    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0


@define
class TimePerTurn:
    """The amount of time passed between turns and the range of turn numbers that this duration applies to."""  # noqa: E501 | None

    years_per_turn: int
    until_turn: int


@define
class VictoryPriorities:
    """Policy branch's priorities for each victory type."""

    neutral: int = 0
    cultural: int = 0
    diplomatic: int = 0
    domination: int = 0
    scientific: int = 0


@define
class BaseTerrain:
    """Base terrains that can appear on the map."""

    name: str
    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    unbuildable: bool = False
    impassable: bool = False
    movement_cost: int = 1
    defence_bonus: float = 0
    rgb: RGBColour = Factory(lambda: RGBColour(r=255, g=215, b=0))
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Belief:
    """Beliefs that can be chosen for religions."""

    name: str
    type: BeliefEnum  # noqa: A003
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Building:
    """Buildings and wonders."""

    name: str
    cost: int | None = None  # see TechColumn, only if cost is -1 ¯\_(ツ)_/¯
    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    maintenance: int = field(default=cast(int, 0), validator=_ge0)
    iswonder: bool = False
    is_national_wonder: bool = False
    required_building: str = ""
    cannot_be_buitt_with: str = ""
    provides_free_building: str = ""
    required_tech: str = ""
    required_resource: str = ""
    required_nearby_improved_resources: list[str] = Factory(list)
    replaces: str = ""
    unique_to: str = ""
    xp_for_new_units: int = field(default=cast(int, 0), validator=_ge0)
    city_strength: int = 0
    city_health: int = 0
    hurry_cost_modifier: int = 0
    quote: str = ""
    uniques: list[str] = Factory(list)
    replacement_text_for_uniques: str = ""
    percent_stat_bonus: PercentStats = Factory(PercentStats)
    great_person_points: dict[str, int] = Factory(dict)
    specialist_slots: dict[str, int] = Factory(dict)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class CityState:
    """City states."""

    name: str
    city_state_type: CityStateEnum
    style: str = ""
    # adjective: str = ""   TODO
    start_bias: list[str] = Factory(list)
    declaring_war: str = ""
    attacked: str = ""
    defeated: str = ""
    inner_colour: RGBColour = Factory(RGBColour)
    outer_colour: RGBColour = Factory(RGBColour)
    unique_name: str = ""
    unique_text: str = ""
    uniques: list[str] = Factory(list)
    cities: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Difficulty:
    """Difficulty levels a player can choose when starting a new game."""

    name: str
    base_happiness: int | None
    extra_happiness_per_luxury: float | None
    research_cost_modifier: float | None
    unit_cost_modifier: float | None
    building_cost_modifier: float | None
    policy_cost_modifier: float | None
    unhappiness_modifier: float | None
    barbarian_bonus: float | None
    player_bonus_starting_units: list[str] = Factory(list)
    ai_city_growrth_modifier: float | None
    ai_unit_cost_modifier: float | None
    ai_bui_iding_cost_modifier: float | None
    ai_wonder_cost_modifier: float | None
    ai_building_maintenance_modifier: float | None
    ai_unit_maintenance_modifier: float | None
    ai_free_techs: list[str] = Factory(list)
    ai_major_civ_bonus_starting_units: list[str] = Factory(list)
    ai_city_state_bonus_starting_units: list[str] = Factory(list)
    ai_unhappiness_modifier: float | None
    # ais_exchange_techs: bool  # unimplemented  # noqa: ERA001
    tum_barbarians_can_enter_player_tiles: int | None
    clear_barbarian_camp_reward: int | None


@define
class Era:
    """Eras are usually group technologies together and change gameplay."""

    name: str
    research_agreement_cost: int | None
    icon_rgb: RGBColour | None
    unit_base_buy_cost: int | None
    starting_settler_count: int | None
    starting_settler_unit: str | None
    starting_worker_count: int | None
    starting_worker_unit: str | None
    starting_military_unit_count: int | None
    starting_military_unit: str | None
    starting_gold: int | None
    starting_culture: int | None
    settler_population: list[str] = Factory(list)
    settler_buildings: list[str] = Factory(list)


@define
class Feature:
    """Features that can appear on the base terrains in the map."""

    name: str
    occurs_on: list[str] = Factory(list)
    food: int = 0
    production: int = 0
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
class GlobalQuest:
    """Quests that may be given to all major Civilizations by City States."""

    name: str
    description: str
    influence: float = 40
    duration: int = 0
    minimum_civs: int = 1


@define
class GlobalUniques:
    """Defines uniques that apply globally."""

    name: str | None
    uniques: list[str] = Factory(list)


@define
class Improvement:
    """Improvements that can be constructed or created on a map tile by a unit."""  # noqa: E501 | None

    name: str
    terrains_can_be_found_on: list[str] = Factory(list)
    tech_required: str = ""
    unique_to: str = ""
    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    turns_to_build: int | None = field(
        default=cast(int | None, None), validator=_validate_none(_ge0)
    )
    uniques: list[str] = Factory(list)
    shortcut_key: str = field(
        default=cast(str, ""), validator=validators.max_len(1)
    )
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class IndividualQuest:
    """Quests that may be given to one major Civilizations by City States."""

    name: str
    description: str
    influence: float = 40
    duration: int = 0


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


@define
class ModConstants:
    """Collection of constants used internally in Unciv."""

    max_xp_from_barbarians: int = 30
    city_strength_base: float = 8
    city_strength_per_pop: float = 0.4
    city_strength_from_techs_multiplier: float = 5.5
    city_strength_from_techs_exponent: float = 2.8
    city_strength_from_techs_full_multip_iier: float = 1.0
    city_strength_from_garrison: float = 0.2
    unit_supply_per_population: float = 0.5
    minimal_city_distance: int = 3
    minimak_city_distance_on_different_continents: int = 2
    unit_upgrade_cost: UnitUpgradeCost = Factory(UnitUpgradeCost)
    natural_wonder_count_multiplier: float = 0.124
    natural_wonder_count_added_constant: float = 0.1
    ancient_ruin_count_mu_itip_iier: float = 0.02
    max_lake_size: int = 10
    river_count_multiplier: float = 0.01
    min_river_length: int = 5
    max_river_length: int = 666  # 😈😈😈
    religion_limit_base: int = 1
    religion_limit_multiplier: float = 0.5
    pantheon_base: int = 10
    pantheon_growth: int = 5


@define
class ModOptions:
    """Metadata and mod-wide options for compatibility."""

    is_base_ruleset: bool = False
    uniques: list[str] = Factory(list)
    techs_to_remove: list[str] = Factory(list)
    buildings_to_remove: list[str] = Factory(list)
    units_to_remove: list[str] = Factory(list)
    nations_to_remove: list[str] = Factory(list)
    last_updated: str | None
    mod_url: str | None
    author: str | None
    mod_size: int | None
    constants: ModConstants | None


@define
class Nation:
    """Nations and city states, including Barbarians and Spectator."""

    name: str
    leader_name: str = ""
    style: str = ""
    # adjective: str = ""   TODO
    start_bias: list[str] = Factory(list)
    preferred_victory_type: VictoryGoalEnum = VictoryGoalEnum.Neutral
    start_intro_part1: str = ""
    start_intro_part2: str = ""
    declaring_war: str = ""
    attacked: str = ""
    defeated: str = ""
    introduction: str = ""
    neutral_hello: str = ""
    hate_hello: str = ""
    trade_request: str = ""
    inner_colour: RGBColour = Factory(RGBColour)
    outer_colour: RGBColour = Factory(RGBColour)
    unique_name: str = ""
    unique_text: str = ""
    uniques: list[str] = Factory(list)
    cities: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class NaturalWonder:
    """NaturalWonders that can appear on the base terrains in the map."""

    name: str
    occurs_on: list[str] = Factory(list)
    turns_into: str = ""
    weight: int = 10
    food: int = 0
    production: int = 0
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
class Policy:
    """Available social policies that can be "bought" with culture."""

    name: str
    era: str
    priorities: VictoryPriorities = Factory(VictoryPriorities)
    uniques: list[str] = Factory(list)
    policies: list[PolicyMember] = Factory(list)


@define
class Promotion:
    """Available unit promotions."""

    name: str
    prerequisites: str | None
    column: int | None
    row: int | None
    unit_types: list[str] = Factory(list)
    uniques: list[str] = Factory(list)
    civilopedia_text: list[CivilopediaText] = Factory(list)


class Religion(str):  # must have image
    """Strings specifying all predefined Religion names."""

    __slots__: tuple[()] = ()


@define
class Resource:
    """Resources that a map tile can have."""

    name: str
    resource_type: ResourceEnum = ResourceEnum.Bonus
    terrains_can_be_found_on: list[str] = Factory(list)
    food: int = 0
    production: int = 0
    gold: int = 0
    science: int = 0
    culture: int = 0
    happiness: int = 0
    faith: int = 0
    improvement: str = ""
    improvement_stats: Stats = Factory(Stats)
    revealed_by: str = ""
    unique: str = ""
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class Ruin:
    """Possible rewards ancient ruins give."""

    name: str
    notification: str
    weight: int | None
    uniques: list[str] = Factory(list)
    excluded_diffculties: list[str] = Factory(list)
    color: RGBColour = Factory(RGBColour)


@define
class Specialist:
    """Specialists that populations of a city can be put into."""

    name: str
    food: int = 0
    production: int = 0
    gold: int = 0
    culture: int = 0
    science: int = 0
    faith: int = 0
    colour: RGBColour = Factory(RGBColour)
    great_person_points: dict[str, int] = Factory(dict)


@define
class Speed:
    """Speeds that determine modifiers to adjust the expected number of rounds in a game of Unciv."""  # noqa: E501 | None

    name: str
    modifier: float | None
    production_cost_modifier: float | None
    gold_cost_modifier: float | None
    science_cost_modifier: float | None
    culture_cost_modifier: float | None
    faith_cost_modifier: float | None
    improvement_build_length_modifier: float | None
    barbarian_modifier: float | None
    gold_gift_modifier: float | None
    city_state_tribute_scaling_interval: float | None
    golden_age_length_modifier: float | None
    religious_pressure_adjacent_city: int | None
    peace_deal_duration: int | None
    deal_duration: int | None
    start_year: float | None
    turns: list[TimePerTurn]


@define
class Tech:
    """Technologies that can be researched with science."""

    name: str
    cost: int = 0 # if 0 get from TechColumn
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
    techs: dict[str, Tech]


class TechTree(list[TechColumn]):
    """Technology tree."""


@define
class Tileset:
    """Tilesets used in game."""

    use_colour_as_base_terrain: bool | None
    use_summary_images: bool | None
    unexplored_tile_colour: ColourTileset | None
    fog_of_war_colour: ColourTileset | None
    fallback_tile_set: str | None
    tile_scale: float | None
    tile_scales: dict[str, float] | None
    rule_variants: dict[str, list[str]] | None


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
    cost: int = 0
    movement: int = field(default=cast(int, 0), validator=_ge0)
    strength: int | None
    ranged_strength: int | None
    range: int | None  # noqa: A003
    intercept_range: int | None
    required_tech: str | None
    obsolete_tech: str | None
    required_resource: str | None
    upgrades_to: str | None
    replaces: str | None
    unique_to: str | None
    hurry_cost_modifier: int | None
    promotions: list[str] = Factory(list)
    uniques: list[str] = Factory(list)
    replacement_text_for_uniques: str | None
    attack_sound: str | None
    civilopedia_text: list[CivilopediaText] = Factory(list)


@define
class UnitType:
    """Units, both military and civilian."""

    name: str
    movement_type: str
    uniques: list[str] = Factory(list)


@define
class UncivMod:
    base_terrains: list[BaseTerrain] = Factory(list)
    beliefs: dict[str, Belief] = Factory(dict)
    buildings: dict[str, Building] = Factory(dict)
    city_states: dict[str, CityState] = Factory(dict)
    difficulties: dict[str, Difficulty] = Factory(dict)
    eras: dict[str, Era] = Factory(dict)
    features: list[Feature] = Factory(list)
    global_uniques: list[GlobalUniques] = Factory(list)
    global_quests: dict[str, GlobalQuest] = Factory(dict)
    improvements: dict[str, Improvement] = Factory(dict)
    individual_quests: dict[str, IndividualQuest] = Factory(dict)
    mod_constants: ModConstants = Factory(ModConstants)
    nations: dict[str, Nation] = Factory(dict)
    natural_wonders: list[NaturalWonder] = Factory(list)
    policies: dict[str, Policy] = Factory(dict)
    promotions: dict[str, Promotion] = Factory(dict)
    religions: list[Religion] = Factory(list)
    resources: dict[str, Resource] = Factory(dict)
    ruins: dict[str, Ruin] = Factory(dict)
    specialists: dict[str, Specialist] = Factory(dict)
    speeds: dict[str, Speed] = Factory(dict)
    techs: TechTree = Factory(TechTree)
