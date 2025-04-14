from typing import Union


def syntax_exception(line: int) -> SyntaxError:
    return SyntaxError("invalid syntax at line "+str(line))

def definition_exception(var_name: str, line: int) -> NameError:
    return NameError(var_name+ " isn't defined at line "+str(line))

def type_exception(var_name: str, expected_type: Union[type, str], line: int) -> TypeError:
    type_name = "nb" if expected_type in (float, int) else ("str" if expected_type == str else ("bool" if expected_type == bool else ("list" if expected_type == list else str(expected_type))))
    return TypeError(var_name + " isn't a " + type_name +" at line "+ str(line))