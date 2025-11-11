import pathlib

import constants
import custominput
import data
import team


def get_mode() -> str:
    return custominput.try_until_in(
        lambda: custominput.input_quit(
            'Write or read team? "w" for write and "r" for read. ',
        ),
        ("w", "r"),
        "Invalid mode selected, please try again.",
    )


def write_mode() -> None:
    new_team = team.team_factory()
    print(new_team)
    data.write_team(
        new_team,
        pathlib.Path(constants.TEAM_PATH / f"{new_team.name}.json"),
    )


def read_mode() -> None:
    loaded_team = team.load_team()
    print(loaded_team)


def main() -> None:
    print(f"gtpr by r5ne!\nat any point type {constants.EXIT_VALUE} to quit safely")
    while True:
        mode = get_mode()
        match mode:
            case "w":
                write_mode()
            case "r":
                read_mode()
            case _:
                pass


if __name__ == "__main__":
    main()
