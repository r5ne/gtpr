import pathlib

import constants
import custominput
import data
import pydantic


class Team(pydantic.BaseModel):
    name: str
    skill: str
    characters: list[Character]


class Character(pydantic.BaseModel):
    name: str


def character_factory(character_slots_available: list[str]) -> tuple[Character, str]:
    print(
        "Starting character creation process...\n"
        f"Free character slots: {character_slots_available}",
    )
    name = custominput.input_quit("Character name: ")
    index = custominput.try_until_in(
        lambda: custominput.input_quit("Team slot: "),
        character_slots_available,
        "Character slot already occupied, please try another slot.",
    )
    return Character(name=name), index


def team_factory(unique_name: str) -> Team:
    print("Starting team creation process...")
    skill = custominput.try_until_in(
        lambda: custominput.input_quit("Team skill: "),
        constants.SKILL,
        f"Invalid skill rating, must be part of {constants.SKILL}",
    )
    characters_to_add = ["1", "2", "3", "4"]
    characters = {}
    while characters_to_add:
        character, str_index = character_factory(characters_to_add)
        characters_to_add.remove(str_index)
        index = int(str_index)
        characters[index] = character

    character_list = [characters[i] for i in sorted(characters.keys())]
    # model_construct doesn't have the overhead of validating data, and since it's
    # already been validated, skipping calling model_validate saves performance
    return Team.model_construct(
        name=unique_name, skill=skill, characters=character_list
    )


def check_if_team_exists() -> pathlib.Path:
    while True:
        name = custominput.input_quit("Team name: ")
        path = pathlib.Path(constants.TEAM_PATH / f"{name}.json")
        if not path.exists():
            return path
        print("Team already exists! Try another team name, or read the team.")


def make_team() -> None:
    while True:
        team_path = check_if_team_exists()
        new_team = team_factory(team_path.stem)
        data.write_team(new_team, team_path)


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
