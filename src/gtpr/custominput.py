import sys
from typing import TYPE_CHECKING, Any, Literal, overload

import constants

if TYPE_CHECKING:
    from collections.abc import Callable

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


@overload
def get_valid_input[T: Any](
    txt: str,
    parser: Callable[[str], tuple[T, bool]],
    validator: InputValidator | None = ...,
) -> T: ...


@overload
def get_valid_input(
    txt: str,
    parser: None = ...,
    *,
    validator: InputValidator,
) -> str: ...


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


@overload
def get_valid_multi_line_input(
    txt: str,
    parser: None = ...,
    *,
    validator: InputValidator,
    allow_partial_errors: bool = ...,
) -> list[str]: ...


@overload
def get_valid_multi_line_input[T: Any](
    txt: str,
    parser: Callable[[str], tuple[T, bool]],
    validator: InputValidator | None = ...,
    *,
    allow_partial_errors: bool = ...,
) -> list[T]: ...


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


def combine_validators(
    *validators: InputValidator,
    log_all_errors: bool = True,
) -> InputValidator:
    def combined(value: Any) -> InputValidatorReturn:
        error_msgs = ""
        for validator in validators:
            valid, error_msg = validator(value)
            if valid:
                continue
            if not log_all_errors:
                assert error_msg, str
                return False, error_msg
            error_msgs += f"{error_msg}\n"

        if error_msgs:
            return False, error_msgs
        return True, None

    return combined


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


def type_parser_factory(new_type: type) -> Callable[[str], tuple[Any, bool]]:
    return parser_factory(
        lambda txt: new_type(txt), ValueError, f"Input is not of type {new_type}."
    )


def str_method_parser_factory[TStr: str, TAny: Any](
    str_method: Callable[[TStr], TAny] = str.lower,
) -> Callable[[TStr], tuple[TAny, Literal[True]]]:
    return lambda txt: (str_method(txt), True)
