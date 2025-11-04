from typing import Literal
import pathlib

import team


def make_team() -> team.Team | Literal[False]:
    name = input_quit("name: ")
    skill = input_quit("skill: ")
    if not (name and skill):
        return False
    else:
        return team.Team(name, "good")


def input_quit(txt: str) -> str | Literal[False]:
    output = input(txt)
    if output == "\\q":
        return False
    else:
        return output


def main() -> None:
    running = True
    print("gtpr by r5ne!\nat any point type \\q to quit safely")
    while running:
        if not (team := make_team()):
            running = False
        else:
            team.mk_new_file(pathlib.Path())


if __name__ == "__main__":
    main()
