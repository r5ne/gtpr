import sys
from typing import TYPE_CHECKING, Any, Literal, overload

import constants

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

type InputValidatorReturn = tuple[Literal[False], str] | tuple[Literal[True], None]
type InputValidator = Callable[[Any], InputValidatorReturn]


def input_quit(txt: str) -> str:
    output = input(txt)
    if output == constants.EXIT_VALUE:
        sys.exit()
    return output


def multi_line_input_quit(txt: str) -> list[str]:
    print(
        "The following input allows for pasting/writing multi-line data. On a blank new"
        "line type 'CTRL+Z' on windows or 'CTRL+D' on unix and send with ENTER to save "
        "the input"
    )
    lines = [input_quit(txt)]
    while True:
        try:
            line = input_quit("")
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


def get_valid_input[T: Any](
    txt: str,
    parser: Callable[[str], tuple[T, bool]] | None = None,
    validator: InputValidator | None = None,
) -> T | str:
    while True:
        output = input_quit(txt)
        if parser is not None:
            output, successful = parser(output)
            if not successful:
                print(output)
                continue
        if validator is not None:
            valid, err_msg = validator(output)
            if not valid:
                print(err_msg)
                continue
        return output


def get_valid_multi_line_input[T: Any](
def get_valid_multi_line_input[T: Any](
    txt: str,
    parser: Callable[[str], tuple[T, bool]] | None = None,
    validator: InputValidator | None = None,
    *,
    allow_partial_errors: bool = False,
) -> list[T] | list[str]:
    while True:
        output_lines = multi_line_input_quit(txt)
        output = []
        invalid_line = False
        for line in output_lines:
            current_line = line
            if parser is not None:
                current_line, successful = parser(current_line)
                if not successful:
                    print(current_line)
                    if allow_partial_errors:
                        continue
                    invalid_line = True
                    break
            if validator is not None:
                valid, err_msg = validator(current_line)
                if not valid:
                    print(err_msg)
                    if allow_partial_errors:
                        continue
                    invalid_line = True
                    break
            output.append(current_line)
        if invalid_line and not allow_partial_errors:
            continue
        return output




def validator_factory[T: Any](
    check_func: Callable[[T], bool], false_func_msg: str
) -> InputValidator:
    def validator(value: T) -> InputValidatorReturn:
        if check_func(value):
            return True, None
        return False, false_func_msg

    return validator


def parser_factory[Txt: str](
    parser_func: Callable[[Txt], Any],
    error: type[BaseException],
    parser_failed_msg: str,
) -> Callable[[Txt], tuple[Any, bool]]:
    def parser(txt: Txt) -> tuple[Any, bool]:
        try:
            return parser_func(txt), True
        except error:
            return parser_failed_msg, False

    return parser
