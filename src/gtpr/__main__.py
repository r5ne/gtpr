import pathlib
import sys
from typing import Literal

import data
import team

TEAM_PATH = pathlib.Path.cwd() / "teams"
EXIT_VALUE = "\\q"


def input_quit(txt: str) -> str:
    output = input(txt)
    if output == EXIT_VALUE:
        sys.exit()
    return output


def team_factory() -> team.Team:
    name = input_quit("name: ")
    return team.Team(name=name)


def get_mode() -> Literal["w", "r"]:
    while (
        answer := input_quit('Write or read team? "w" for write and "r" for read.')
    ) not in (
        "w",
        "r",
    ):
        print("Invalid mode selected, please try again.")
    return answer


def make_team() -> None:
    while True:
        new_team = team_factory()
        try:
            data.write_team(new_team, TEAM_PATH / f"{new_team.name}.json")
        except FileExistsError:
            print("Team already exists! Try another team name, or read the team.")
        else:
            return


def load_team() -> team.Team:
    while True:
        team_name = input_quit("Enter the name of your team to load: ")
        team_path = TEAM_PATH / f"{team_name}.json"
        try:
            loaded_team = data.read_team(team_path)
        except FileNotFoundError:
            print(f"Team not found at path: {team_path}. Try a different team name")
        else:
            return loaded_team


def main() -> None:
    print(f"gtpr by r5ne!\nat any point type {EXIT_VALUE} to quit safely")
    while True:
        mode = get_mode()
        match mode:
            case "w":
                make_team()
            case "r":
                loaded_team = load_team()
                print(loaded_team.__str__())


if __name__ == "__main__":
    main()
