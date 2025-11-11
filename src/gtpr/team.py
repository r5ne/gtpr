import pathlib

import constants
import custominput
import data
import pydantic


class Team(pydantic.BaseModel):
    name: str
    skill: str
    characters: list[Character]
    character_dps_substat_importance: list[float] = [0, 0, 0, 0]
    character_field_time_percent: list[float]
    avg_active_character_health: float = 0
    effective_shield_health: int
    shield_health_relevance: float = 0
    character_shield_health_substat_importance: list[float] = [0, 0, 0, 0]
    abs_character_optimal_substat_dps_diff: list[float] = [0, 0, 0, 0]
    dps_vs_sustain_mult: float = 1

    def update_character_dps_substat_importance(self) -> None:
        total_substat_dps_diff = sum(
            self.characters[i].no_substat_dps_diff for i in range(4)
        )
        for i, character in enumerate(self.characters):
            self.character_dps_substat_importance[i] = round(
                (character.no_substat_dps_diff / total_substat_dps_diff) * 100, 2
            )

    def update_abs_character_optimal_substat_dps_diff(self) -> None:
        for i, character in enumerate(self.characters):
            self.abs_character_optimal_substat_dps_diff[i] = round(
                character.optimal_substat_dps_diff
                * self.character_dps_substat_importance[i]
                / 100,
                2,
            )

    def update_avg_active_character_health(self) -> None:
        self.avg_active_character_health = round(
            sum(
                self.character_field_time_percent[i] * character.health
                for i, character in enumerate(self.characters)
            )
            / 1.04
        )

    def update_shield_health_relevance(self) -> None:
        self.shield_health_relevance = round(
            self.effective_shield_health / self.avg_active_character_health,
            2,
        )

    def update_character_shield_health_substat_importance(self) -> None:
        for i, character in enumerate(self.characters):
            self.character_shield_health_substat_importance[i] = round(
                self.shield_health_relevance * character.no_substat_shield_health_diff,
                2,
            )


class Character(pydantic.BaseModel):
    name: str
    health: int
    no_substat_dps_diff: float
    optimal_substat_dps_diff: float
    no_substat_shield_health_diff: float


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
    health = int(custominput.input_quit("Character health: "))
    no_substat_dps_diff = float(
        custominput.input_quit("Character no substat dps diff: ")
    )
    optimal_substat_dps_diff = float(
        custominput.input_quit("Character optimal substat dps diff: ")
    )
    no_substat_shield_health_diff = float(
        custominput.input_quit("Character no substat shield health diff: ")
    )
    field_time_percent = float(custominput.input_quit("Character field time percent: "))
    return (
        Character(
            name=name,
            health=health,
            no_substat_dps_diff=no_substat_dps_diff,
            optimal_substat_dps_diff=optimal_substat_dps_diff,
            no_substat_shield_health_diff=no_substat_shield_health_diff,
        ),
        field_time_percent,
        index,
    )


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
    effective_shield_health = int(
        custominput.input_quit("Team effective shield health: ")
    )

    # model_construct doesn't have the overhead of validating data, and since it's
    # already been validated, skipping calling model_validate saves performance
    new_team = Team.model_construct(
        name=name,
        skill=skill,
        characters=character_list,
        character_field_time_percent=character_field_time_percent_list,
        effective_shield_health=effective_shield_health,
    )
    calculate_team_dps(new_team)
    calculate_team_shield_health(new_team)
    return new_team


def new_team_name() -> str:
    while True:
        name = custominput.input_quit("Team name: ")
        path = pathlib.Path(constants.TEAM_PATH / f"{name}.json")
        if not path.exists():
            return path.stem
        print("Team already exists! Try another team name, or read the team instead.")


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


def calculate_team_dps(team: Team) -> None:
    team.update_character_dps_substat_importance()
    team.update_abs_character_optimal_substat_dps_diff()


def calculate_team_shield_health(team: Team) -> None:
    team.update_avg_active_character_health()
    team.update_shield_health_relevance()
    team.update_character_shield_health_substat_importance()
