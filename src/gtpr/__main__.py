import sys
from typing import TYPE_CHECKING, Any

import constants
import data
import team

if TYPE_CHECKING:
    from collections.abc import Callable


def input_quit(txt: str) -> str:
    output = input(txt)
    if output == constants.EXIT_VALUE:
        sys.exit()
    return output


def require_output_in_tuple[T](
    value: Callable[..., T],
    required_outputs: tuple[Any, ...],
    invalid_msg: str,
) -> T:
    while (output := value()) not in required_outputs:
        print(invalid_msg)
    return output


def team_factory() -> team.Team:
    name = input_quit("name: ")
    skill = require_output_in_tuple(
        lambda: input_quit("skill: "),
        constants.SKILL,
        f"Invalid skill rating, must be part of {constants.SKILL}",
    )
    return team.Team(name=name, skill=skill)


def get_mode() -> str:
    return require_output_in_tuple(
        lambda: input_quit('Write or read team? "w" for write and "r" for read.'),
        ("w", "r"),
        "Invalid mode selected, please try again.",
    )


def make_team() -> None:
    while True:
        new_team = team_factory()
        try:
            data.write_team(new_team, constants.TEAM_PATH / f"{new_team.name}.json")
        except FileExistsError:
            print("Team already exists! Try another team name, or read the team.")
        else:
            return


def load_team() -> team.Team:
    while True:
        team_name = input_quit("Enter the name of your team to load: ")
        team_path = constants.TEAM_PATH / f"{team_name}.json"
        try:
            loaded_team = data.read_team(team_path)
        except FileNotFoundError:
            print(f"Team not found at path: {team_path}. Try a different team name")
        else:
            return loaded_team


def main() -> None:
    print(f"gtpr by r5ne!\nat any point type {constants.EXIT_VALUE} to quit safely")
    while True:
        mode = get_mode()
        match mode:
            case "w":
                make_team()
            case "r":
                loaded_team = load_team()
                print(loaded_team)
            case _:
                pass


if __name__ == "__main__":
    main()
