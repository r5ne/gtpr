from typing import Literal

import team


def make_team() -> team.Team | Literal[False]:
    name = input_quit("name: ")
    if not name:
        return False
    else:
        return team.Team(name)


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
            print(team)


if __name__ == "__main__":
    main()
