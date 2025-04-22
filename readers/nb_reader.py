from memory_variables import to_float, parentheses_extractor
from errors import syntax_exception


def nb_reader(code_line: str, line: int) -> int:
    while "(" in code_line:
        parentheses_extractor_output = parentheses_extractor(code_line, line)
        code_line = (code_line[:code_line.index("(")] +
                     str(nb_reader(parentheses_extractor_output[0], line)) +
                     code_line[parentheses_extractor_output[1]+1:])

    number = ""
    operation = ""
    nb = 0
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
    if operation == "+": nb += to_float(number, line)
    elif operation == "-": nb -= to_float(number, line)
    elif operation == "*": nb *= to_float(number, line)
    elif operation == "/": nb /= to_float(number, line)
    elif operation == "^": nb **= to_float(number, line)
    elif operation == "%": nb %= to_float(number, line)
    elif operation == "": nb = to_float(number, line)
    else: raise syntax_exception(line)
    return nb
