from typing import cast

from memory_variables import parentheses_extractor, get_soft_typed_var, get_type
from errors import syntax_exception


def to_float(string: str, line: int) -> float:
    if string.strip() != "":
        if len(string.split(".")) < 3:
            if len(tuple(filter(lambda char: not (char.isdigit() or char == "."), string))) == 0:
                return float(string)
        if not string.strip()[0].isdecimal():
            if get_type(string, line) in (bool, str, float):
                return float(cast(float | str | bool, get_soft_typed_var(string, line)))
    raise syntax_exception(string, line, "invalid syntax for integer")

def nb_reader(code_line: str, line: int) -> float:
    while "(" in code_line:
        parentheses_extractor_output = parentheses_extractor(code_line, line)
        code_line = (code_line[:code_line.index("(")] +
                     str(nb_reader(parentheses_extractor_output[0], line)) +
                     code_line[parentheses_extractor_output[1]+1:])

    number = ""
    operation = ""
    result = 0.0
    for char in code_line:
        if not (char.isdigit() or char=="."):
            if char in ("+", "-", "*", "/", "^", "%"):
                if operation == "+":
                    result += to_float(number, line)
                elif operation == "-":
                    result -= to_float(number, line)
                elif operation == "*":
                    result *= to_float(number, line)
                elif operation == "/":
                    result /= to_float(number, line)
                elif operation == "^":
                    result **= to_float(number, line)
                elif operation == "%":
                    result %= to_float(number, line)
                else:
                    result = to_float(number, line)
                operation = char
                number = ""
            else:
                number += char
        else:
            number += char
    if operation == "+":
        result += to_float(number, line)
    elif operation == "-":
        result -= to_float(number, line)
    elif operation == "*":
        result *= to_float(number, line)
    elif operation == "/":
        result /= to_float(number, line)
    elif operation == "^":
        result **= to_float(number, line)
    elif operation == "%":
        result %= to_float(number, line)
    elif operation == "":
        result = to_float(number, line)
    else:
        raise syntax_exception(code_line, line)
    return result
