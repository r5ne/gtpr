import pathlib

import constants
import custominput
import data
import team


def get_mode() -> str:
    validator = custominput.validator_factory(
        lambda txt: txt in {"w", "r"}, "Invalid mode selected, please try again."
    )
    return custominput.get_valid_input(
        "Write or read team? 'w' for write and 'r' for read. ",
        parser=custominput.str_method_parser_factory(),
        validator=validator,
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
    validator = custominput.validator_factory(
        lambda txt: txt in {"v", "e", "r"}, "Invalid mode selected, please try again."
    )
    read_mode = custominput.get_valid_input(
        "Team successfully loaded!\nView team, edit team or recalculate data? 'v' "
        "for view, 'e' for edit and 'r' for recalculate.",
        parser=custominput.str_method_parser_factory(),
        validator=validator,
    )
    match read_mode:
        case "v":
            print(loaded_team)
        case "e":
            ...
        case _:
            pass


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
