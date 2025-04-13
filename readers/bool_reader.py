from typing import Tuple, Optional
from memory_variables import _bool, _str, _nb
from errors import syntax_exception, definition_exception
from readers import nb_reader, str_reader


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

def bool_operation_handler(bool_1: bool, operation: str, bool_2: bool, line: int) -> bool:
    if operation == "or": return bool_1 or bool_2
    if operation == "and": return bool_1 and bool_2
    if operation == "xor": return bool_1 ^ bool_2
    if operation == "nor": return not (bool_1 or bool_2)
    if operation == "nand": return not (bool_1 and bool_2)
    if operation == "nxor": return not (bool_1 ^ bool_2)
    else: raise syntax_exception(line)

def bool_reader(code_line: str, line: int) -> bool:
    while "(" in code_line:
        code_line = (code_line[:code_line.index("(")] + " " +
                     str(bool_reader(parentheses_extractor(code_line, line)[0], line)) +
                     " " + code_line[parentheses_extractor(code_line, line)[1] + 1:])

    precedent_bool: Optional[bool] = None
    operation = ""
    inversion = False
    for word in list(filter(lambda x: x!="", code_line.split(" "))):
        if word == "True":
            if precedent_bool is None:
                precedent_bool = not inversion
                inversion = False
            else:
                precedent_bool = bool_operation_handler(precedent_bool, operation, not inversion, line)
                operation, inversion = "", False
        elif word == "False":
            if precedent_bool is None:
                precedent_bool = inversion
                inversion = False
            else:
                precedent_bool = bool_operation_handler(precedent_bool, operation, inversion, line)
                operation, inversion = "", False
        elif word == "not": inversion = not inversion
        elif word in ["or", "and", "xor", "nor", "nand", "nxor"]: operation = word
        elif word in _bool:
            if precedent_bool is None:
                precedent_bool = inversion ^ _bool[word]
                inversion = False
            else:
                precedent_bool = bool_operation_handler(precedent_bool, operation, inversion ^ _bool[word], line)
                operation, inversion = "", False
        else: raise definition_exception(word, line)
    if operation!="" or inversion: raise syntax_exception(line)
    return precedent_bool

def check_reader(code_line: str, line: int) -> bool:
    code_line = "".join(list(filter(lambda x: x!=" ", [a for a in code_line])))

    if "==" in code_line:
        if code_line.split("==")[0] in _nb:
            if code_line.split("==")[1] in _nb:
                param_2 = nb_reader.nb_reader(code_line.split("==")[1], line)
            else: return False
            param_1 = _nb[code_line.split("==")[0]]
        elif code_line.split("==")[0] in _str:
            if code_line.split("==")[1] in _str:
                param_2 = str_reader.str_reader(code_line.split("==")[1], line)
            else: return False
            param_1 = _str[code_line.split("==")[0]]
        elif code_line.split("==")[0] in _bool:
            if code_line.split("==")[1] in _bool:
                param_2 = bool_reader(code_line.split("==")[1], line)
            else: return False
            param_1 = _bool[code_line.split("==")[0]]
        else: raise definition_exception(code_line.split("==")[0], line)

        return param_1 == param_2

    elif "!=" in code_line:
        if code_line.split("!=")[0] in _nb: param_1 = _nb[code_line.split("!=")[0]]
        elif code_line.split("!=")[0] in _str: param_1 = _str[code_line.split("!=")[0]]
        elif code_line.split("!=")[0] in _bool: param_1 = _bool[code_line.split("!=")[0]]
        else: raise definition_exception(code_line.split("!=")[0], line)

        if code_line.split("!=")[1] in _nb: param_2 = _nb[code_line.split("!=")[1]]
        elif code_line.split("!=")[1] in _str: param_2 = _str[code_line.split("!=")[1]]
        elif code_line.split("!=")[1] in _bool: param_2 = _bool[code_line.split("!=")[1]]
        else: raise definition_exception(code_line.split("!=")[1], line)

        return param_1 != param_2

    elif "<=" in code_line:
        if code_line.split("<=")[0] in _nb: param_1 = _nb[code_line.split("<=")[0]]
        elif code_line.split("<=")[0] in _str: param_1 = _str[code_line.split("<=")[0]]
        elif code_line.split("<=")[0] in _bool: param_1 = _bool[code_line.split("<=")[0]]
        else: raise definition_exception(code_line.split("<=")[0], line)

        if code_line.split("<=")[1] in _nb: param_2 = _nb[code_line.split("<=")[1]]
        elif code_line.split("<=")[1] in _str: param_2 = _str[code_line.split("<=")[1]]
        elif code_line.split("<=")[1] in _bool: param_2 = _bool[code_line.split("<=")[1]]
        else: raise definition_exception(code_line.split("<=")[1], line)

        return param_1 <= param_2

    elif ">=" in code_line:
        if code_line.split(">=")[0] in _nb: param_1 = _nb[code_line.split(">=")[0]]
        elif code_line.split(">=")[0] in _str: param_1 = _str[code_line.split(">=")[0]]
        elif code_line.split(">=")[0] in _bool: param_1 = _bool[code_line.split(">=")[0]]
        else: raise definition_exception(code_line.split(">=")[0], line)

        if code_line.split(">=")[1] in _nb: param_2 = _nb[code_line.split(">=")[1]]
        elif code_line.split(">=")[1] in _str: param_2 = _str[code_line.split(">=")[1]]
        elif code_line.split(">=")[1] in _bool: param_2 = _bool[code_line.split(">=")[1]]
        else: raise definition_exception(code_line.split(">=")[1], line)

        return param_1 >= param_2

    elif "<" in code_line:
        if code_line.split("<")[0] in _nb: param_1 = _nb[code_line.split("<")[0]]
        elif code_line.split("<")[0] in _str: param_1 = _str[code_line.split("<")[0]]
        elif code_line.split("<")[0] in _bool: param_1 = _bool[code_line.split("<")[0]]
        else: raise definition_exception(code_line.split("<")[0], line)

        if code_line.split("<")[1] in _nb: param_2 = _nb[code_line.split("<")[1]]
        elif code_line.split("<")[1] in _str: param_2 = _str[code_line.split("<")[1]]
        elif code_line.split("<")[1] in _bool: param_2 = _bool[code_line.split("<")[1]]
        else: raise definition_exception(code_line.split("<")[1], line)

        return param_1 < param_2

    elif ">" in code_line:
        if code_line.split(">")[0] in _nb: param_1 = _nb[code_line.split(">")[0]]
        elif code_line.split(">")[0] in _str: param_1 = _str[code_line.split(">")[0]]
        elif code_line.split(">")[0] in _bool: param_1 = _bool[code_line.split(">")[0]]
        else: raise definition_exception(code_line.split(">")[0], line)

        if code_line.split(">")[1] in _nb: param_2 = _nb[code_line.split(">")[1]]
        elif code_line.split(">")[1] in _str: param_2 = _str[code_line.split(">")[1]]
        elif code_line.split(">")[1] in _bool: param_2 = _bool[code_line.split(">")[1]]
        else: raise definition_exception(code_line.split(">")[1], line)

        return param_1 > param_2

    else: raise syntax_exception(line)