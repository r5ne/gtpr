import pathlib
import uuid

import calc
import constants
import custominput
import data
import gcslparser
import pydantic


class Build(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: uuid.uuid4().hex)
    weapon: str
    energy_recharge: float


class Character(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: uuid.uuid4().hex)

    name: str
    best_artifact_sets: list[str]
    artifact_set: str
    builds: list[Build] = []


class TeamBuild(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: uuid.uuid4().hex)
    builds: dict[str, str]
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
    team_builds: list[TeamBuild] = []
    active_team_build_id: str | None = None


        )
    )


        )
        )
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
    validate_skill = custominput.validator_factory(
        lambda txt: txt in constants.SKILL,
        f"Invalid skill rating, must be part of {constants.SKILL}",
    )
    skill = custominput.get_valid_input(
        "Team skill: ",
        parser=custominput.str_method_parser_factory(),
        validator=validate_skill,
    )
    characters_to_add = [1, 2, 3, 4]
    characters = {}
    character_field_time_percent = {}
    print("Starting character creation process...")
    while characters_to_add:
        print(f"Free character slots: {characters_to_add}")

        validate_char_slot = custominput.validator_factory(
            lambda num: num in characters_to_add,
            "Character slot already occupied, please try another slot.",
        )
        index = custominput.get_valid_input(
            "Team slot: ",
            parser=custominput.type_parser_factory(int),
            validator=validate_char_slot,
        )
        character = character_factory()
        characters[index] = character

        field_time_percent = custominput.get_valid_input(
            "Character field time percent: ", custominput.type_parser_factory(float)
        )
        character_field_time_percent[index] = field_time_percent

        characters_to_add.remove(index)
    character_list = [characters[i] for i in sorted(characters.keys())]
    character_field_time_percent_list = [
        character_field_time_percent[i]
        for i in sorted(character_field_time_percent.keys())
    ]
    return Team.model_construct(
        name=name,
        skill=skill,
        characters=character_list,
        character_field_time_percent=character_field_time_percent_list,
    )


def character_factory() -> Character:
    name = custominput.input_quit("Character name: ")
    current_artifact_set = custominput.input_quit("Character current artifact set: ")
    return Character.model_construct(
        name=name,
        best_artifact_sets=[current_artifact_set],
        artifact_set=current_artifact_set,
    )


def add_build(characters: list[Character]) -> None:
    print("Starting new build creation process...")
    while True:
        config = custominput.multi_line_input_quit(
            "Paste in your gcsl character config generated from genshin optimiser."
        )
        config = gcslparser.normalise_optimal_character_config(config)
        character_details = gcslparser.get_character_details(config)
        try:
            add_details_to_character(characters, character_details)
        except ValueError:
            print(
                "Character config pasted (character name: "
                f"{character_details['character']} doesn't match any of the characters "
                f"present in the team: {[char.name for char in characters]}."
            )
        else:
            return


def add_details_to_character(
    characters: list[Character], details: dict[str, str]
) -> None:
    for character in characters:
        if str.lower(character.name) != details["character"]:
            continue
        character.builds.append(
            Build.model_construct(
                weapon=details["weapon"],
            )
        )
        if (arti_set := details["artifact_set"]) in character.best_artifact_sets:
            character.best_artifact_sets.insert(
                0,
                character.best_artifact_sets.pop(
                    character.best_artifact_sets.index(arti_set)
                ),
            )
        else:
            character.best_artifact_sets.insert(0, arti_set)
        return
    raise ValueError


def add_team_build(team: Team) -> None:
    print(f"Starting new team build creation process for team: {team.name}...")
    builds = {}
    character_no_substat_dps = {}
    character_optimal_artifact_dps = {}
    for character in team.characters:
        validate_in_build = custominput.validator_factory(
            lambda index, char=character: index in set(range(len(char.builds))),
            "Build index out of range.",
        )
        index = custominput.get_valid_input(
            f"From the current available builds for {character.name}: "
            f"{character.builds}, give the index of the build to use for this team: ",
            parser=custominput.type_parser_factory(int),
            validator=validate_in_build,
        )
        builds[character.id] = character.builds[index].id
        no_substat_dps = custominput.get_valid_input(
            "Character no substat dps: ", custominput.type_parser_factory(float)
        )
        character_no_substat_dps[character.id] = no_substat_dps
        optimal_artifact_dps = custominput.get_valid_input(
            "Character optimal artifact & substat dps: ",
            custominput.type_parser_factory(float),
        )

        character_optimal_artifact_dps[character.id] = optimal_artifact_dps
    team_dps = custominput.get_valid_input(
        "Team dps: ", custominput.type_parser_factory(int)
    )
    new_team_build = TeamBuild(
        builds=builds,
        team_dps=team_dps,
        character_no_substat_dps=character_no_substat_dps,
        character_optimal_artifact_dps=character_optimal_artifact_dps,
    )
    calc.calculate_dps_diffs(team, new_team_build)
    calc.calculate_substat_importance(team, new_team_build)

    team.team_builds.append(new_team_build)
    if team.active_team_build_id is not None:
        validate_yesno = custominput.validator_factory(
            lambda txt: txt in {"y", "n"},
            "Invalid answer, requires 'y' or 'n' as an answer",
        )
        update_team_build_to_current = custominput.get_valid_input(
            "Update active build to current build? 'y' for yes, 'n' for no: ",
            validator=validate_yesno,
        )
        if update_team_build_to_current == "n":
            return
    set_active_team_build(team, new_team_build)


def set_active_team_build(team: Team, build: TeamBuild) -> None:
    if not build.character_substat_importance:
        msg = "Build has not had its values calculated yet, cannot activate team build."
        raise ValueError(msg)
    team.active_team_build_id = build.id


def get_active_team_build(team: Team) -> TeamBuild:
    return next(
        build for build in team.team_builds if build.id == team.active_team_build_id
    )


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
