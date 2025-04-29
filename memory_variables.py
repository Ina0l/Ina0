from typing import Dict, List, Tuple, Union
from errors import definition_exception, type_exception, syntax_exception

_nb: Dict[str, float] = {}
_str: Dict[str, str] = {}
_bool: Dict[str, bool] = {}
_list: Dict[str, list] = {}
_funct: Dict[str, Tuple[List[str], Tuple[str], int]] = {}

def to_float(string: str, line: int) -> float:
    try:
        return float(string)
    except ValueError:
        try:
            return float(get_var(string, line))
        except NameError:
            raise definition_exception(string, line)
        except ValueError:
            raise type_exception(string, float, line)

def get_var(string: str, line: int) -> Union[float, str, bool, list]:
    if string == "": raise syntax_exception(line)
    elif string in ("True", "true"): return True
    elif string == ("False", "false"): return False
    elif string in _str: return _str[string]
    elif string in _nb: return _nb[string]
    elif string in _bool: return _bool[string]
    elif string in _list: return _list[string]
    else: raise definition_exception(string, line)

def delete_var(var: str) -> None:
    if var in _str: _str.pop(var)
    if var in _nb: _nb.pop(var)
    if var in _bool: _bool.pop(var)
    if var in _list: _list.pop(var)

def delete_other_instance(var_name: str, var_type: type) -> None:
    if var_type in (float, int):
        if var_name in _str: _str.pop(var_name)
        if var_name in _bool: _bool.pop(var_name)
        if var_name in _list: _list.pop(var_name)
    if var_type == str:
        if var_name in _nb: _nb.pop(var_name)
        if var_name in _bool: _bool.pop(var_name)
        if var_name in _list: _list.pop(var_name)
    if var_type == bool:
        if var_name in _str: _str.pop(var_name)
        if var_name in _nb: _nb.pop(var_name)
        if var_name in _list: _list.pop(var_name)
    if var_type == list:
        if var_name in _str: _str.pop(var_name)
        if var_name in _bool: _bool.pop(var_name)
        if var_name in _nb: _nb.pop(var_name)

def set_var(var_name: str, value: Union[float, str, bool, list]) -> None:
    if value is None: return
    if type(value) == float: _nb.update({var_name: value})
    if type(value) == str: _str.update({var_name: value})
    if type(value) == bool: _bool.update({var_name: value})
    if type(value) == list: _list.update({var_name: value})

def get_type(code: str, line: int) -> type:
    if " or " in code or " nor " in code or " and " in code or " nand " in code or " xor " in code or " nxor " in code or "not " in code:
        for operator in (" or ", " nor ", " and ", " nand ", " xor ", " nxor ", "not "):
            if operator in code:
                indexes = get_indexes(code, operator) + get_indexes(code, "\"")
                indexes.sort()
                quote_opened = False
                for index in indexes:
                    if index in get_indexes(code, operator):
                        if not quote_opened: return bool
                    elif index in get_indexes(code, "\""):
                        quote_opened = False if quote_opened else False
    elif " == " in code or " != " in code or " <= " in code or " >= " in code or " < " in code or " > " in code:
        for operator in (" == ", " != ", " <=> ", " >= ", " < ", " > "):
            if operator in code:
                indexes = get_indexes(code, operator) + get_indexes(code, "\"")
                indexes.sort()
                quote_opened = False
                for index in indexes:
                    if index in get_indexes(code, operator):
                        if not quote_opened: return bool
                    elif index in get_indexes(code, "\""):
                        quote_opened = False if quote_opened else False
    elif "\"" in code: return str
    else:
        if "+" in code or "-" in code or "*" in code or "/" in code or "^" in code or "%" in code:
            return float
        elif len(code.split()) > 1:
            return str
        elif code == "": raise syntax_exception(line)
        elif code[0].isdigit(): return float
        else: return type(get_var(no_space(code), line))

def get_indexes(string: str, sub: str) -> List[int]:
    if string.count(sub) == 0: raise ValueError(f"'{sub}' is not in list")
    indexes = []
    if string.rindex(sub) == len(string) - len(sub) - 1: indexes.append(len(string) - len(sub) - 1)
    index = 0
    for substring in string.split(sub):
        index += len(substring)
        indexes.append(index)
        index += len(sub)
    indexes = sorted(indexes[:-1])
    return indexes

def no_space(string: str) -> str:
    return "".join(string.split())

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
    raise syntax_exception(line_nb)

def slice_quote_apart(string: str, sub: str) -> List[str]:
    quote_opened = False
    sub_string = ""
    sliced_string = []
    current_slice = ""
    for char in string:
        if char == "\"": quote_opened = False if quote_opened else True
        if char == sub[len(sub_string)] and not quote_opened:
            sub_string += char
            if sub_string == sub:
                sliced_string.append(current_slice)
                current_slice = ""
                sub_string = ""
        else:
            current_slice += char
            sub_string = ""
    sliced_string.append(current_slice)
    return sliced_string


def insert_spaces(string: str) -> str:
    spaced_string = ""
    for index in range(len(string)):
        if (index != len(string)-1 and string[index] in ("=", "!") and string[index + 1] == "=") or string[index] in ("<", ">"):
            spaced_string += " "
        spaced_string += string[index]
        if (index != 0 and string[index] == "=" and string[index - 1] in ("=", "!", "<", ">")) or (index != len(string) - 1 and string[index] in ("<", ">") and string[index + 1] != "="):
            spaced_string += " "
    return " ".join(spaced_string.split())
