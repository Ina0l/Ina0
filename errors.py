from typing import Union


def syntax_exception(expr: str, line: int) -> SyntaxError:
    return SyntaxError(f"invalid syntax '{expr}' at line {line}")

def definition_exception(var_name: str, line: int) -> NameError:
    return NameError(f"'{var_name}' isn't defined at line {line}")

def type_exception(var_name: str, expected_type: Union[type, str], line: int) -> TypeError:
    type_name = "nb" if expected_type in (float, int) else ("str" if expected_type == str else ("bool" if expected_type == bool else ("list" if expected_type == list else expected_type)))
    return TypeError(f"'{var_name}' isn't a {str(type_name).replace("|", "or")} at line {line}")

def type_exception_with_value(var_name: str, value, expected_type: Union[type, str], line: int) -> TypeError:
    type_name = "nb" if expected_type in (float, int) else ("str" if expected_type == str else ("bool" if expected_type == bool else ("list" if expected_type == list else expected_type)))
    return TypeError(f"'{var_name}' with value {value} isn't a {str(type_name).replace("|", "or")} at line {line}")