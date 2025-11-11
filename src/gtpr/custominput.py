import sys
from typing import TYPE_CHECKING, Any

import constants

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


def input_quit(txt: str) -> str:
    output = input(txt)
    if output == constants.EXIT_VALUE:
        sys.exit()
    return output


def multi_line_input_quit(txt: str) -> list[str]:
    print(
        "The following input allows for pasting/writing multi-line data. "
        "Type 'CTRL+Z' on windows or 'CTRL+D' on unix to save the input"
    )
    lines = [input(txt)]
    while True:
        try:
            line = input()
        except EOFError:
            return lines
        lines.append(line)


def try_until_in[T](
    input_func: Callable[..., T],
    required: Iterable[Any],
    not_in_msg: str,
) -> T:
    while (output := input_func()) not in required:
        print(not_in_msg)
    return output


def try_until_no_error[T](
    input_func: Callable[..., T],
    error: type[BaseException],
    error_occured_msg: str,
) -> T:
    while True:
        try:
            output = input_func()
        except error:
            print(error_occured_msg)
        else:
            return output
