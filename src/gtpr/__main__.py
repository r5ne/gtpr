import constants
import custominput
import team


def get_mode() -> str:
    return custominput.try_until_in(
        lambda: custominput.input_quit(
            'Write or read team? "w" for write and "r" for read. ',
        ),
        ("w", "r"),
        "Invalid mode selected, please try again.",
    )


def main() -> None:
    print(f"gtpr by r5ne!\nat any point type {constants.EXIT_VALUE} to quit safely")
    while True:
        mode = get_mode()
        match mode:
            case "w":
                team.make_team()
            case "r":
                loaded_team = team.load_team()
                print(loaded_team)
            case _:
                pass


if __name__ == "__main__":
    main()
