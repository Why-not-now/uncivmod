from __future__ import annotations

import copy
import json
import logging
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

from PIL import Image

# _vanilla = ("Civ V - Gods & Kings", "Civ V - Vanilla")
type JSONDict = dict[str, Any]
type TechDict = dict[str, int]

_ignore_files = ("ModOptions.json",)
uniques_all = []
uniques_avoid = []


def prettify_json(path: Path, output: Path | None) -> None:
    contents = path.read_text(encoding="utf-8")
    contents = re.sub(r"/\*(?:.|\s)*?\*/", r"", contents)  # multiline comment
    contents = re.sub(r"//.*?(?=\n|$)", r"", contents)  # singleline comment
    contents = re.sub(r",(?=\s*[\]\}])", r"", contents)  # trailing comma
    contents = re.sub(
        r"(?<=[0-9\]\}\"])"
        r"(?=\s*(?=[\[\{]|\"[^\"]*\")([^\"]*\"[^\"]*\")*[^\"]*$)",
        r",",
        contents,
    )  # expected comma
    if output is None:
        output = path

    try:
        output.write_text(
            json.dumps(json.loads(contents), indent="\t", ensure_ascii=False),
            encoding="UTF-8",
        )
    except json.decoder.JSONDecodeError:
        logging.debug(path)
        logging.debug(contents)
        raise


def format_json(json_file: Path, output_dir: Path, mod_name: str) -> None:
    if json_file.name in _ignore_files:
        return

    if json_file.suffix != ".json":
        return

    output_folder = output_dir / mod_name / "jsons"
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder / json_file.name
    output_file.touch()
    prettify_json(json_file, output_file)


def uniques_paramless(unique_file: Path) -> list[str]:
    with unique_file.open(encoding="UTF-8") as f:
        uniques = f.read().splitlines()

    logging.debug([re.sub(r"\[.*?\]", r"[]", x) for x in uniques])
    return [re.sub(r"\[.*?\]", r"[]", x) for x in uniques]


def clean_mods(input_dir: Path, output_dir: Path, parent_dir: Path) -> None:
    for mod_dir in input_dir.iterdir():
        if not mod_dir.is_dir():
            continue

        json_dir = mod_dir / "jsons"

        for json_file in (json_dir).iterdir():
            format_json(json_file, output_dir, mod_dir.name)

        shutil.copytree(
            mod_dir / "Images",
            output_dir / mod_dir.name / "Images",
            dirs_exist_ok=True,
        )

        shutil.copytree(
            mod_dir / "Images",
            parent_dir / "Combined" / "Images",
            dirs_exist_ok=True,
        )

        shutil.copyfile(
            mod_dir / "credits.md", output_dir / mod_dir.name / "credits.md"
        )


class Combined:
    def __init__(self) -> None:
        self.nations: JSONDict = {
            "name": "Upside-Down",
            "leaderName": "Rotatceps",
            "adjective": ["Upside-Down"],
            "style": "Upside Down",
            "startIntroPart1": "History in best the among generals and soldiers its, other the to world the of end one from battle into triumphantly marched have armies its.nation great a as endured has Down-Upside - enemies often and - competitors by surrounded although. Letters and arts, culture of center world the been Down-Upside has long. Rotatceps, you to triumph and life long.",
            "startIntroPart2": "Time of test the stand will that civilization a build you can? World the of center again once Down-Upside make you will? All to order and peace bringing, again rises empire your that it to see you will? Down-Upside of glory the reclaim more once to you to turn people your, Rotatceps mighty O?",
            "declaringWar": "Time payback it's, now. It know you, badly very yourself behaved you've.",
            "attacked": "It swear I! Dearly regret soon will you! Fool!",
            "defeated": "Triumph your in merciful be will you hope I. Yours is...day the.",
            "introduction": "Bravery military for renowned are who, you with relationship just and fair a for hope we.",
            "neutralHello": "Peace you wish I.",
            "hateHello": "Want you do what?",
            "tradeRequest": "Me with deal this make to - existing for reason a have do you that appears it.",
            "outerColor": [255, 255, 255],
            "innerColor": [0, 0, 0],
            "uniqueName": "The World Turned Upside-Down",
            "uniqueText": "All the special advantages that other nations have, combined into one, with none of the special disadvantages. Are you ready to turn the world upside down?",
            "uniques": [],
            "cities": [],
            "spyNames": [],
        }
        self.buildings: dict[str, JSONDict] = {}
        self._base_buildings: dict[str, JSONDict] = {}
        self.improvements: dict[str, JSONDict] = {}
        self.units: dict[str, JSONDict] = {}
        self._base_units: dict[str, JSONDict] = {}
        self.tech: TechDict = {}

    def set_tech(self, tech: list[JSONDict]) -> None:
        self.tech = clean_tech(tech)

    def add_nation(self, nation: JSONDict) -> None:
        if "cityStateType" in nation:
            return

        self.nations = update_uniques(self.nations, nation)

        if "cities" in nation:
            city_reverse: str = nation["cities"][0][::-1].lower().capitalize()
            if city_reverse not in self.nations["cities"]:
                self.nations["cities"].append(city_reverse)

        if "spyNames" in nation:
            spy_reverse: str = nation["spyNames"][0][::-1].lower().capitalize()
            if spy_reverse not in self.nations["spyNames"]:
                self.nations["spyNames"].append(spy_reverse)

    def add_building(self, building: JSONDict) -> None:
        if "replaces" not in building:
            self._base_buildings[building["name"]] = building
            return

        base_building: str = building["replaces"]
        if base_building not in self.buildings:
            self.buildings[base_building] = building | {
                "name": base_building[::-1].lower().title(),
                "uniqueTo": "Upside-Down",
            }

        else:
            self.buildings[base_building] = update_building(
                self.buildings[base_building], building, self.tech
            )

    def add_improvement(self, improvement: JSONDict) -> None:
        if "uniqueTo" not in improvement:
            return

        name: str = improvement["name"]
        if name not in self.improvements:
            self.improvements[name] = improvement | {
                "name": name[::-1].lower().capitalize(),
                "uniqueTo": "Upside-Down",
            }

        else:
            self.improvements[name] = update_improvement(
                self.improvements[name], improvement, self.tech
            )

    def add_unit(self, unit: JSONDict) -> None:
        if "replaces" not in unit:
            self._base_units[unit["name"]] = unit
            return

        base_unit: str = unit["replaces"]
        if base_unit not in self.units:
            self.units[base_unit] = unit | {
                "name": base_unit[::-1].lower().title(),
                "uniqueTo": "Upside-Down",
                "unitType": [unit["unitType"]],
            }
            if "upgradesTo" in unit:
                self.units[base_unit]["unitType"] = [
                    (unit["unitType"], unit["upgradesTo"])
                ]
                del self.units[base_unit]["upgradesTo"]
            else:
                self.units[base_unit]["unitType"] = [(unit["unitType"], "")]

        else:
            self.units[base_unit] = update_unit(
                self.units[base_unit], unit, self.tech
            )

    def to_building_json(self, mod_dir: Path) -> list[JSONDict]:
        building_json: list[JSONDict] = []
        for key, item in self.buildings.items():
            if key not in self._base_buildings:
                msg = f'"{key}" not in base buildings'
                raise Exception(msg)

            building_json.append(
                update_building(item, self._base_buildings[key], self.tech)
            )

            Image.open(
                mod_dir / "Images" / "BuildingIcons" / f"{key}.png"
            ).transpose(Image.ROTATE_180).save(
                mod_dir / "Images" / "BuildingIcons" / f"{item["name"]}.png"
            )
        return building_json

    def to_improvement_json(self, mod_dir: Path) -> list[JSONDict]:
        improvement_json: list[JSONDict] = []
        for key, item in self.improvements.items():
            improvement_json.append(item)

            Image.open(
                mod_dir / "Images" / "ImprovementIcons" / f"{key}.png"
            ).transpose(Image.ROTATE_180).save(
                mod_dir / "Images" / "ImprovementIcons" / f"{item["name"]}.png"
            )

            image_file = (
                mod_dir
                / "Images"
                / "TileSets"
                / "FantasyHex"
                / "Tiles"
                / f"{key}.png"
            )
            if image_file.is_file():
                Image.open(image_file).transpose(Image.FLIP_TOP_BOTTOM).save(
                    mod_dir
                    / "Images"
                    / "TileSets"
                    / "FantasyHex"
                    / "Tiles"
                    / f"{item["name"]}.png"
                )

        return improvement_json

    def to_nation_json(self, mod_dir: Path | None = None):
        return [self.nations]

    def to_unit_json(self, mod_dir: Path) -> list[JSONDict]:
        unit_json: list[JSONDict] = []
        for key, item in self.units.items():
            if key not in self._base_units:
                msg = f'"{key}" not in base units'
                raise Exception(msg)

            base_unit = self._base_units[key]
            unit_group: JSONDict = update_unit(item, base_unit, self.tech)
            if "attackSound" in base_unit:
                unit_group |= {"attackSound": base_unit["attackSound"]}

            if "uniques" in item:
                logging.debug(item["name"])
                uniques: list[str] = item["uniques"]
            else:
                uniques: list[str] = []
            u_init_len = len(uniques)
            uniques, all_name = add_transform(uniques, unit_group, base_unit)
            unit_json.extend(
                separate_sub_unit(
                    mod_dir,
                    key,
                    unit_group,
                    base_unit,
                    all_name,
                    uniques,
                    u_init_len,
                )
            )

            for name in all_name:
                Image.open(
                    mod_dir / "Images" / "UnitIcons" / f"{key}.png"
                ).transpose(Image.ROTATE_180).save(
                    mod_dir / "Images" / "UnitIcons" / f"{name}.png"
                )

                image_dir = (
                    mod_dir
                    / "Images"
                    / "TileSets"
                    / "FantasyHex"
                    / "Units"
                    / f"{key}.png"
                )
                if image_dir.is_file():
                    Image.open(image_dir).transpose(
                        Image.FLIP_TOP_BOTTOM
                    ).save(
                        mod_dir
                        / "Images"
                        / "TileSets"
                        / "FantasyHex"
                        / "Units"
                        / f"{name}.png"
                    )

        for key, item in self._base_units.items():
            if key in self.units:
                continue

            image_dir = (
                mod_dir
                / "Images"
                / "TileSets"
                / "FantasyHex"
                / "Units"
                / f"{key}.png"
            )
            if image_dir.is_file():
                Image.open(image_dir).transpose(Image.FLIP_TOP_BOTTOM).save(
                    mod_dir
                    / "Images"
                    / "TileSets"
                    / "FantasyHex"
                    / "Units"
                    / f"{item["name"]}-Upside Down.png"
                )

        return unit_json

    def to_json(
        self, mod_dir: Path, output_dir: Path, default_dic: Path | None = None
    ) -> None:
        json_dir = mod_dir / "jsons"
        for json_file in json_dir.iterdir():
            if json_file.name != "ModOptions.json":
                json_file.unlink()
        for string, func in (
            ("Buildings", self.to_building_json),
            ("Nations", self.to_nation_json),
            ("TileImprovements", self.to_improvement_json),
            ("Units", self.to_unit_json),
        ):
            json_object = func(mod_dir)
            if json_object:
                (mod_dir / "jsons" / f"{string}.json").write_text(
                    json.dumps(json_object, indent="\t"), encoding="UTF-8"
                )
        combine_json(mod_dir, output_dir, default_dic)


def update_building(
    original: JSONDict, replace: JSONDict, tech: TechDict
) -> JSONDict:
    return_json = copy.deepcopy(original)
    gains_attr = [
        "food",
        "production",
        "gold",
        "happiness",
        "culture",
        "science",
        "faith",
        "xpForNewUnits",
        "cityStrength",
    ]
    multi_gains_attr = [
        "percentStatBonus",
        "greatPersonPoints",
        "specialistSlots",
    ]
    costs_attr = ["cost", "maintenance", "hurryCostModifier"]

    for gain in gains_attr:
        return_json = update_gain(gain, return_json, replace)
    for cost in costs_attr:
        return_json = update_cost(cost, return_json, replace)
    for multi_gains in multi_gains_attr:
        return_json = update_multi_gain(multi_gains, return_json, replace)
    return_json = update_uniques(
        return_json, replace, [(return_json["name"], replace["name"])]
    )
    return_json = update_oldest_tech(
        "requiredTech", return_json, replace, tech
    )

    return return_json


def update_improvement(
    original: JSONDict, replace: JSONDict, tech: TechDict
) -> JSONDict:
    return_json = copy.deepcopy(original)
    gains_attr = [
        "food",
        "production",
        "gold",
        "happiness",
        "culture",
        "science",
        "faith",
    ]

    for gain in gains_attr:
        return_json = update_gain(gain, return_json, replace)
    return_json = update_cost("turnsToBuild", return_json, replace)
    return_json = update_uniques(
        return_json, replace, [(replace["name"], original["name"])]
    )
    return_json = update_table("terrainsCanBeBuiltOn", return_json, replace)
    return_json = update_oldest_tech(
        "requiredTech", return_json, replace, tech
    )

    return return_json


def update_unit(
    original: JSONDict, replace: JSONDict, tech: TechDict
) -> JSONDict:
    return_json = copy.deepcopy(original)
    gains_attr = [
        "movement",
        "strength",
        "rangedStrength",
        "range",
        "interceptRange",
        "faith",
    ]
    costs_attr = ["cost", "maintenance", "hurryCostModifier"]

    for gain in gains_attr:
        return_json = update_gain(gain, return_json, replace)
    for cost in costs_attr:
        return_json = update_cost(cost, return_json, replace)
    return_json = update_table("promotions", return_json, replace)
    if "upgradesTo" in replace:
        unit_type = (replace["unitType"], replace["upgradesTo"])
    else:
        unit_type = (replace["unitType"], "")
    return_json["unitType"] = list({*return_json["unitType"], unit_type})
    return_json = update_uniques(
        return_json, replace, [(replace["name"], return_json["name"])]
    )
    return_json = update_oldest_tech(
        "requiredTech", return_json, replace, tech
    )
    return_json = update_newest_tech(
        "obsoleteTech", return_json, replace, tech
    )

    if "requiredResource" in return_json and "requiredResource" not in replace:
        del return_json["requiredResource"]

    return return_json


def update_gain(key: str, original: JSONDict, replace: JSONDict) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in replace and key in return_json:
        return_json[key] = max(return_json[key], replace[key])
    elif key in replace and replace[key] > 0:
        return_json[key] = replace[key]
    elif key in return_json and return_json[key] <= 0:
        del return_json[key]

    return return_json


def update_cost(key: str, original: JSONDict, replace: JSONDict) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in replace and key in return_json:
        return_json[key] = max(return_json[key], replace[key])
    elif key in replace and replace[key] < 0:
        return_json[key] = replace[key]
    elif key in return_json and return_json[key] >= 0:
        del return_json[key]

    return return_json


def update_multi_gain(
    key: str, original: JSONDict, replace: JSONDict
) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in replace and key in return_json:
        gains: set[str] = {*return_json[key], *replace[key]}
        for gain in gains:
            return_json[key] = update_gain(
                gain, return_json[key], replace[key]
            )
    elif key in replace:
        return_json[key] = replace[key]

    return return_json


def update_table(key: str, original: JSONDict, replace: JSONDict) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in replace and key in return_json:
        return_json[key] = list({*return_json[key], *replace[key]})
    elif key in replace:
        return_json[key] = replace[key]

    return return_json


def update_uniques(
    original: JSONDict,
    replace: JSONDict,
    name_replace: Iterable[tuple[str, str]] | None = None,
) -> JSONDict:
    return_json = copy.deepcopy(original)

    if "uniques" not in replace:
        return return_json

    new_uniques: list[str] = replace["uniques"]
    if name_replace is not None and "uniques" in replace:
        for i, unique in enumerate(new_uniques):
            unique: str
            unique_amend = unique
            for new_name, old_name in name_replace:
                unique_amend = unique_amend.replace(old_name, new_name)
            new_uniques[i] = unique_amend

    old_uniques: list[str] = []
    if "uniques" in return_json:
        old_uniques = copy.deepcopy(return_json["uniques"])
    new_uniques = check_uniques(new_uniques)

    combined_uniques = avoid_uniques(old_uniques, new_uniques)
    if combined_uniques:
        return_json["uniques"] = combined_uniques
    elif "uniques" in return_json:
        del return_json["uniques"]

    return return_json


def update_oldest_tech(
    key: str, original: JSONDict, replace: JSONDict, tech: TechDict
) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in return_json and key in replace:
        if tech[return_json[key]] > tech[replace[key]]:
            return_json[key] = replace[key]
    elif key in return_json:
        del return_json[key]

    return return_json


def update_newest_tech(
    key: str, original: JSONDict, replace: JSONDict, tech: TechDict
) -> JSONDict:
    return_json = copy.deepcopy(original)

    if key in return_json and key in replace:
        if tech[return_json[key]] < tech[replace[key]]:
            return_json[key] = replace[key]
    elif key in replace:
        return_json[key] = replace[key]

    return return_json


def clean_tech(tech_tree: list[JSONDict]) -> TechDict:
    tech_cleaned: TechDict = {}
    for column in tech_tree:
        for tech in column["techs"]:
            tech: JSONDict
            tech_cleaned[tech["name"]] = column["columnNumber"]

    return tech_cleaned


def avoid_uniques(old_uniques: list[str], new_uniques: list[str]) -> list[str]:
    old_cleaned_uniques: list[str] = [
        re.sub(r" *\<.*?\>", r"", re.sub(r"\[.*?\]", r"[]", x))
        for x in old_uniques
    ]
    new_cleaned_uniques: list[str] = [
        re.sub(r" *\<.*?\>", r"", re.sub(r"\[.*?\]", r"[]", x))
        for x in new_uniques
    ]

    for unique in uniques_avoid:
        if unique in old_cleaned_uniques and unique not in new_uniques:
            old_uniques.pop(old_cleaned_uniques.index(unique))
        elif unique in new_cleaned_uniques and unique not in old_uniques:
            new_uniques.pop(new_cleaned_uniques.index(unique))

    if old_uniques and new_uniques:
        return list({*old_uniques, *new_uniques})
    if old_uniques:
        return old_uniques
    if new_uniques:
        return new_uniques
    return []


def check_uniques(uniques: list[str]) -> list[str]:
    desirables = []

    logging.debug(uniques)
    for x in uniques:
        cleaned_x = re.sub(r" *\<.*?\>", r"", re.sub(r"\[.*?\]", r"[]", x))
        logging.debug(cleaned_x)
        if cleaned_x not in uniques_all:
            while True:
                keep = input(f'"{x}" is not in the uniques list, keep? "Y/n":')
                if keep.lower() == "y":
                    desirables.append(x)
                    break
                if keep.lower() == "n":
                    break

        else:
            desirables.append(x)

    return desirables


def add_transform(
    uniques: list[str], unit: JSONDict, base_unit: JSONDict
) -> tuple[list[str], list[str]]:
    all_names: list[str] = []
    return_uniques = copy.deepcopy(uniques)
    for unit_type, upgrade in unit["unitType"]:
        name_add: list[str] = []
        unit_type: str
        upgrade: str
        name: str = unit["name"]

        if unit_type != base_unit["unitType"]:
            name_add.append(unit_type)
        if upgrade != "" and (
            "upgradesTo" not in base_unit or upgrade != base_unit["upgradesTo"]
        ):
            name_add.append(upgrade)

        if name_add:
            name += f' ({", ".join(name_add)})'
        return_uniques.append(
            f"Can transform to [{name}] <in [Friendly Land] tiles>"
        )
        all_names.append(name)

    return return_uniques, all_names


def separate_sub_unit(
    mod_dir: Path,
    key: str,
    unit_group: JSONDict,
    base_unit: JSONDict,
    all_name: list[str],
    uniques: list[str],
    u_init_len: int,
) -> list[JSONDict]:
    return_json = []
    for i, (unit_type, upgrade) in enumerate(unit_group["unitType"]):
        unit_type: str
        upgrade: str

        unit_individual = copy.deepcopy(unit_group)
        name: str = all_name[i]
        unit_individual["unitType"] = unit_type
        if upgrade != "":
            unit_individual["upgrade"] = upgrade
        unit_individual["name"] = name
        if len(uniques) > 1:
            unit_individual["uniques"] = (
                uniques[: u_init_len + i] + uniques[u_init_len + i + 1 :]
            )
            if name != base_unit["name"][::-1].lower().title():
                del unit_individual["replaces"]

        Image.open(mod_dir / "Images" / "UnitIcons" / f"{key}.png").transpose(
            Image.ROTATE_180
        ).save(mod_dir / "Images" / "UnitIcons" / f"{name}.png")

        return_json.append(unit_individual)

    return return_json


def combine_json(
    combined_dir: Path, output_dir: Path, default_dic: Path | None = None
) -> None:
    json_dict: defaultdict[str, list[JSONDict]] = defaultdict(list)
    global_dict: JSONDict = {"name": "Global uniques", "uniques": []}
    for mod_dir in output_dir.iterdir():
        if not mod_dir.is_dir():
            continue

        json_dir = mod_dir / "jsons"
        if not (json_dir).is_dir():
            continue

        for json_file in json_dir.iterdir():
            if json_file.suffix != ".json" or json_file.name in _ignore_files:
                continue

            with json_file.open(encoding="UTF-8") as f:
                if json_file.stem == "GlobalUniques":
                    global_dict["uniques"].extend(
                        check_uniques(json.load(f)["uniques"])
                    )
                    continue
                json_dict[json_file.name].extend(json.load(f))

    for key, item in json_dict.items():
        json_file = combined_dir / "jsons" / key
        if json_file.exists():
            with json_file.open(encoding="UTF-8") as f:
                json_dict[json_file.name].extend(json.load(f))

        json_file.write_text(
            json.dumps(item, indent="\t", ensure_ascii=False), encoding="UTF-8"
        )

    if global_dict:
        (combined_dir / "jsons" / "GlobalUniques.json").write_text(
            json.dumps(global_dict, indent="\t", ensure_ascii=False),
            encoding="UTF-8",
        )

    if default_dic is not None:
        shutil.copytree(default_dic, combined_dir, dirs_exist_ok=True)


def main() -> None:
    global uniques_all, uniques_avoid
    parent_dir = Path(__file__).parent
    upside_down = Combined()

    logging.basicConfig(filename=parent_dir / "debug.log", level=logging.DEBUG)
    input_dir = parent_dir / "Input"
    output_dir = parent_dir / "Output"
    uniques_all = uniques_paramless(parent_dir / "uniques" / "uniques.txt")
    uniques_avoid = uniques_paramless(parent_dir / "uniques" / "unwanted.txt")
    shutil.rmtree(parent_dir / "Combined" / "Images")

    game_dir = Path(
        "C:/Users/USER/Documents/Generic folder/unciv-windows64/mods"
    )

    clean_mods(input_dir, output_dir, parent_dir)
    with (output_dir / "Civ V - Gods & Kings" / "jsons" / "Techs.json").open(
        encoding="UTF-8"
    ) as f:
        upside_down.set_tech(json.load(f))

    for mod_dir in output_dir.iterdir():
        if not mod_dir.is_dir():
            continue

        json_dir = mod_dir / "jsons"
        if not json_dir.is_dir():
            continue

        for string, func in (
            ("Buildings", upside_down.add_building),
            ("Nations", upside_down.add_nation),
            ("TileImprovements", upside_down.add_improvement),
            ("Units", upside_down.add_unit),
        ):
            if (json_dir / f"{string}.json").is_file():
                with (json_dir / f"{string}.json").open(encoding="UTF-8") as f:
                    for json_object in json.load(f):
                        json_object: JSONDict
                        func(json_object)

    upside_down.to_json(
        parent_dir / "Combined", output_dir, parent_dir / "Default"
    )

    shutil.rmtree(game_dir / "Combined")
    shutil.copytree(
        parent_dir / "Combined",
        game_dir / "Combined",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("*.git"),
    )


if __name__ == "__main__":
    main()
