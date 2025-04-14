from typing import Tuple, List
from memory_variables import _bool, _str, _nb, _list
from errors import syntax_exception, definition_exception
from readers import nb_reader, str_reader


def get_type(code: str) -> type:
    try:
        return type(nb_reader.nb_reader(code, 0))
    except:
        try:
            return type(bool_reader(code, 0))
        except:
            try:
                return type(str_reader.str_reader(code, 0))
            except:
                return type(None)

def parentheses_extractor(code_line: str, line_nb: int) -> Tuple[str, int]:
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
            if opened_parenthesis < 0: raise syntax_exception(line_nb)
            if opened_parenthesis == 0:
                return inter_parenthesis_code[:-1], last_parenthesis_index

def bool_operation_handler(bool_1: bool, operation: str, bool_2: bool, line_nb: int) -> bool:
    if operation == "or": return bool_1 or bool_2
    if operation == "and": return bool_1 and bool_2
    if operation == "xor": return bool_1 ^ bool_2
    if operation == "nor": return not (bool_1 or bool_2)
    if operation == "nand": return not (bool_1 and bool_2)
    if operation == "nxor": return not (bool_1 ^ bool_2)
    else: raise syntax_exception(line_nb)

def bool_reader(line: str, line_nb: int) -> bool:
    while "(" in line:
        line = (line[:line.index("(")] + " " +
                     str(bool_reader(parentheses_extractor(line, line_nb)[0], line_nb)) +
                     " " + line[parentheses_extractor(line, line_nb)[1] + 1:])

    code_line: List[str] = list(filter(lambda x: x!="", line.split(" ")))
    if "or" in code_line or "nor" in code_line or "and" in code_line or "nand" in code_line or "xor" in code_line or "nxor" in code_line:
        indexes = []
        if "or" in code_line: indexes.append(code_line.index("or"))
        if "nor" in code_line: indexes.append(code_line.index("nor"))
        if "and" in code_line: indexes.append(code_line.index("and"))
        if "nand" in code_line: indexes.append(code_line.index("nand"))
        if "xor" in code_line: indexes.append(code_line.index("xor"))
        if "nxor" in code_line: indexes.append(code_line.index("nxor"))
        index = min(indexes)
        arg1 = bool_reader(" ".join(code_line[:index]), line_nb)
        arg2 = bool_reader(" ".join(code_line[index + 1:]), line_nb)
        return bool_operation_handler(arg1, code_line[index], arg2, line_nb)
    elif "==" in code_line or "!=" in code_line or "<" in code_line or "<=" in code_line or ">" in code_line or ">=" in code_line:
        indexes = []
        if "==" in code_line: indexes.append(code_line.index("=="))
        if "!=" in code_line: indexes.append(code_line.index("!="))
        if "<" in code_line: indexes.append(code_line.index("<"))
        if ">" in code_line: indexes.append(code_line.index(">"))
        if "<=" in code_line: indexes.append(code_line.index("<="))
        if ">=" in code_line: indexes.append(code_line.index(">="))
        index = min(indexes)
        arg1 = " ".join(code_line[:index])
        arg2 = " ".join(code_line[index + 1:])
        return check_reader(arg1, code_line[index], arg2, line_nb)
    elif len(code_line) == 1:
        if code_line[0] in _bool: return _bool[code_line[0]]
        elif code_line[0] in ("False", "false"): return False
        elif code_line [0] == ("True", "true"): return True
        elif code_line[0] in _str or code_line[0] in _nb or code_line[0] in _list: raise TypeError(code_line[0] + " isn't bool type at line_nb "+str(line_nb))
        else: raise definition_exception(code_line[0], line_nb)
    elif len(code_line) > 1:
        if code_line[0] == "not":
            return not bool_reader(" ".join(code_line[1:]), line_nb)
    else: raise syntax_exception(line_nb)

def check_reader(value1: str, operation: str, value2: str, line_nb: int) -> bool:
    if operation == "==":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 == param_2

    elif operation == "!=":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 != param_2

    elif operation == "<=":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 <= param_2

    elif operation == ">=":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 >= param_2

    elif operation == "<":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 < param_2

    elif operation == ">":
        if get_type(value1) == float:
            param_1 = nb_reader.nb_reader(value1, line_nb)
            param_2 = nb_reader.nb_reader(value2, line_nb)
        elif get_type(value1) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 >= param_2

    else: raise syntax_exception(line_nb)