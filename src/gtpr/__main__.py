import pathlib
from typing import Literal

import team
import data

DEFAULT_PATH = pathlib.Path.cwd() / "teams"


def make_team() -> team.Team | Literal[False]:
    name = input_quit("name: ")
    if not name:
        return False
    return team.Team(name=name)


def input_quit(txt: str) -> str | Literal[False]:
    output = input(txt)
    if output == "\\q":
        return False
    return output


def main() -> None:
    running = True
    print("gtpr by r5ne!\nat any point type \\q to quit safely")
    while running:
        if not (team := make_team()):
            running = False
        elif not data.write_team(team, DEFAULT_PATH / f"{team.name}.json"):
            print("Team already exists!")


if __name__ == "__main__":
    main()
