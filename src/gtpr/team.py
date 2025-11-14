import pathlib

import constants
import custominput
import data
import pydantic


class Build(pydantic.BaseModel):
    weapon: str
    energy_recharge: float


class TeamBuild(pydantic.BaseModel):
    team_dps: int
    character_no_substat_dps: dict[str, int]
    character_optimal_artifact_dps: dict[str, int]
    character_no_substat_dps_diff: dict[str, int] = {}
    character_no_substat_optimal_dps_diff: dict[str, int] = {}
    team_no_substat_optimal_dps_diff: int = 0
    relative_character_substat_power: dict[str, float] = {}
    absolute_character_substat_power: dict[str, float] = {}
    character_substat_importance: dict[str, float] = {}
    # character_health: dict[str, int]
    # avg_active_character_health: int
    # effective_shield_health: int
    # character_no_substat_shield_health: dict[str, int]
    # shield_health_relevance: int
    # character_shield_health_substat_importance: dict[str, int]


class Team(pydantic.BaseModel):
    name: str
    skill: str
    characters: list[Character]
    character_field_time_percent: list[float]
    dps_vs_sustain_mult: float = 1

        )


        )
        )


class Character(pydantic.BaseModel):
    name: str


def character_factory(
    character_slots_available: list[int],
) -> tuple[Character, float, int]:
    print(
        "Starting character creation process...\n"
        f"Free character slots: {character_slots_available}",
    )
    name = custominput.input_quit("Character name: ")
    index = custominput.try_until_in(
        lambda: int(custominput.input_quit("Team slot: ")),
        character_slots_available,
        "Character slot already occupied, please try another slot.",
    )
    field_time_percent = float(custominput.input_quit("Character field time percent: "))
    return (
        Character(
            name=name,
        ),
        field_time_percent,
        index,
    )
def new_team_name() -> str:
    while True:
        name = custominput.input_quit("Team name: ")
        path = pathlib.Path(constants.TEAM_PATH / f"{name}.json")
        if not path.exists():
            return path.stem
        print("Team already exists! Try another team name, or read the team instead.")


def team_factory() -> Team:
    print("Starting team creation process...")
    name = new_team_name()
    skill = custominput.try_until_in(
        lambda: custominput.input_quit("Team skill: "),
        constants.SKILL,
        f"Invalid skill rating, must be part of {constants.SKILL}",
    )
    characters_to_add = [1, 2, 3, 4]
    characters = {}
    character_field_time_percent = {}
    while characters_to_add:
        character, field_time_percent, index = character_factory(characters_to_add)
        characters_to_add.remove(index)
        characters[index] = character
        character_field_time_percent[index] = field_time_percent
    character_list = [characters[i] for i in sorted(characters.keys())]
    character_field_time_percent_list = [
        character_field_time_percent[i]
        for i in sorted(character_field_time_percent.keys())
    ]

    # model_construct doesn't have the overhead of validating data, and since it's
    # already been validated, skipping calling model_validate saves performance
    new_team = Team.model_construct(
        name=name,
        skill=skill,
        characters=character_list,
        character_field_time_percent=character_field_time_percent_list,
    )
    return new_team


    while True:


def load_team() -> Team:
    while True:
        team_name = custominput.input_quit("Enter the name of your team to load: ")
        team_path = constants.TEAM_PATH / f"{team_name}.json"
        try:
            jsondata = data.read_team(team_path)
        except FileNotFoundError:
            print(f"Team not found at path: {team_path}. Try a different team name")
        else:
            return Team.model_validate_json(jsondata)
