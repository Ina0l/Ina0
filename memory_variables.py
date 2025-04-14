from typing import Dict, List, Tuple, Union
from errors import definition_exception

_nb: Dict[str, float] = {}
_str: Dict[str, str] = {}
_bool: Dict[str, bool] = {}
_list: Dict[str, list] = {}
_funct: Dict[str, Tuple[List[str], int]] = {}

def to_float(string: str, line: int) -> float:
    try:
        return float(string)
    except ValueError:
        try:
            return _nb[string]
        except KeyError:
            raise definition_exception(string, line)

def get_var(string: str, line: int) -> Union[float, str, bool, list]:
    if string == "true": return True
    elif string == "false": return False
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
    if type(value) == float: _nb.update({var_name: value})
    if type(value) == str: _str.update({var_name: value})
    if type(value) == bool: _bool.update({var_name: value})
    if type(value) == list: _list.update({var_name: value})