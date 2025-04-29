from memory_variables import _bool, _str, _nb, _list, get_type, get_var, no_space, parentheses_extractor, insert_spaces
from errors import syntax_exception, definition_exception, type_exception
from readers import nb_reader, str_reader


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

    code_line = insert_spaces(line).split()
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
    elif "not" in code_line and code_line[0] == "not":
        return not bool_reader(" ".join(code_line[1:]), line_nb)
    elif "==" in code_line or "!=" in code_line or "<" in code_line or "<=" in code_line or ">" in code_line or ">=" in code_line or "in" in code_line:
        indexes = []
        if "==" in code_line: indexes.append(code_line.index("=="))
        if "!=" in code_line: indexes.append(code_line.index("!="))
        if "<" in code_line: indexes.append(code_line.index("<"))
        if ">" in code_line: indexes.append(code_line.index(">"))
        if "<=" in code_line: indexes.append(code_line.index("<="))
        if ">=" in code_line: indexes.append(code_line.index(">="))
        if "in" in code_line: indexes.append(code_line.index("in"))
        index = min(indexes)
        arg1 = " ".join(code_line[:index])
        arg2 = " ".join(code_line[index + 1:])
        return check_reader(arg1, code_line[index], arg2, line_nb)
    elif len(code_line) == 1:
        if code_line[0] in _bool: return _bool[code_line[0]]
        elif code_line[0] in ("False", "false"): return False
        elif code_line [0] in ("True", "true"): return True
        elif code_line[0] in _str or code_line[0] in _nb or code_line[0] in _list: raise type_exception(code_line[0], bool, line_nb)
        else: raise definition_exception(code_line[0], line_nb)
    else:
        print(code_line)
        raise syntax_exception(line_nb)

def check_reader(value1: str, operation: str, value2: str, line_nb: int) -> bool:
    if operation == "==":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        elif get_type(value1, line_nb) == list:
            param_1 = get_var(value1, line_nb)
            param_2 = get_var(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 == param_2

    elif operation == "!=":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        elif get_type(value1, line_nb) == list:
            param_1 = get_var(value1, line_nb)
            param_2 = get_var(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 != param_2

    elif operation == "<=":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 <= param_2

    elif operation == ">=":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 >= param_2

    elif operation == "<":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 < param_2

    elif operation == ">":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
            param_2 = nb_reader.nb_reader(no_space(value2), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
            param_2 = bool_reader(value2, line_nb)
        else: raise definition_exception(value1, line_nb)

        return param_1 > param_2

    elif operation == "in":
        if get_type(value1, line_nb) == float:
            param_1 = nb_reader.nb_reader(no_space(value1), line_nb)
        elif get_type(value1, line_nb) == str:
            param_1 = str_reader.str_reader(value1, line_nb)
        elif get_type(value1, line_nb) == bool:
            param_1 = bool_reader(value1, line_nb)
        elif get_type(value1, line_nb) == list:
            param_1 = get_var(value1, line_nb)
        else: raise definition_exception(value1, line_nb)

        if get_type(value2, line_nb) == str:
            param_2 = str_reader.str_reader(value2, line_nb)
        elif get_type(value2, line_nb) == list:
            param_2 = get_var(value2, line_nb)
        else:
            if get_type(value2, line_nb) in (float, bool):
                raise type_exception(value2, "str or list", line_nb)
            else: raise definition_exception(value2, line_nb)

        return param_1 in param_2

    else: raise syntax_exception(line_nb)