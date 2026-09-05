from memory_variables import parentheses_extractor, get_var
from errors import syntax_exception


def to_float(string: str, line: int) -> float:
    try:
        return float(string)
    except ValueError as error:
        if string.strip()[0].isdecimal():
            raise error
        return float(get_var(string, line, float))


def nb_reader(code_line: str, line: int) -> float:
    while "(" in code_line:
        parentheses_extractor_output = parentheses_extractor(code_line, line)
        code_line = (code_line[:code_line.index("(")] +
                     str(nb_reader(parentheses_extractor_output[0], line)) +
                     code_line[parentheses_extractor_output[1]+1:])

    number = ""
    operation = ""
    nb = 0.0
    for char in code_line:
        if not (char.isdigit() or char=="."):
            if char in ("+", "-", "*", "/", "^", "%"):
                if operation == "+":
                    nb += to_float(number, line)
                elif operation == "-":
                    nb -= to_float(number, line)
                elif operation == "*":
                    nb *= to_float(number, line)
                elif operation == "/":
                    nb /= to_float(number, line)
                elif operation == "^":
                    nb **= to_float(number, line)
                elif operation == "%":
                    nb %= to_float(number, line)
                else:
                    nb = to_float(number, line)
                operation = char
                number = ""
            else:
                number += char
        else:
            number += char
    if operation == "+":
        nb += to_float(number, line)
    elif operation == "-":
        nb -= to_float(number, line)
    elif operation == "*":
        nb *= to_float(number, line)
    elif operation == "/":
        nb /= to_float(number, line)
    elif operation == "^":
        nb **= to_float(number, line)
    elif operation == "%":
        nb %= to_float(number, line)
    elif operation == "":
        nb = to_float(number, line)
    else:
        raise syntax_exception(code_line, line)
    return nb
