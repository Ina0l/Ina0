from typing import Tuple
import memory_variables
from errors import syntax_exception


def parentheses_extractor(code_line: str, line: int) -> Tuple[str, int]:
    opened_parenthesis = 0
    inter_parenthesis_code = ""
    in_parenthesis = False
    last_parenthesis_index = -1
    for char in code_line:
        last_parenthesis_index += 1
        if in_parenthesis: inter_parenthesis_code += char
        if char == "(":
            in_parenthesis = True
            opened_parenthesis += 1
        if char == ")":
            opened_parenthesis -= 1
            if opened_parenthesis < 0: raise syntax_exception(line)
            if opened_parenthesis == 0:
                return inter_parenthesis_code[:-1], last_parenthesis_index

def nb_reader(code_line: str, line: int) -> int:
    while "(" in code_line:
        code_line = (code_line[:code_line.index("(")] +
                     str(nb_reader(parentheses_extractor(code_line, line)[0], line)) +
                     code_line[parentheses_extractor(code_line, line)[1]+1:])

    number = ""
    operation = ""
    nb = 0
    for char in code_line:
        if not (char.isdigit() or char=="."):
            if char in ["+", "-", "*", "/", "^"]:
                if operation == "+":
                    nb += memory_variables.to_float(number, line)
                    operation = ""
                elif operation == "-":
                    nb -= memory_variables.to_float(number, line)
                    operation = ""
                elif operation == "*":
                    nb *= memory_variables.to_float(number, line)
                    operation = ""
                elif operation == "/":
                    nb /= memory_variables.to_float(number, line)
                    operation = ""
                elif operation == "^":
                    nb **= memory_variables.to_float(number, line)
                    operation = ""
                else:
                    nb = memory_variables.to_float(number, line)
                    operation = char
                    number = ""
            else:
                number += char
        else:
            number += char
    if operation == "+": nb += memory_variables.to_float(number, line)
    elif operation == "-": nb -= memory_variables.to_float(number, line)
    elif operation == "*": nb *= memory_variables.to_float(number, line)
    elif operation == "/": nb /= memory_variables.to_float(number, line)
    elif operation == "^": nb **= memory_variables.to_float(number, line)
    elif operation == "": nb = memory_variables.to_float(number, line)
    else: raise syntax_exception(line)
    return nb
