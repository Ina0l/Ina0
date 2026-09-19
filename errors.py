from typing import Type, cast


def syntax_exception(expr: str, line: int, error_message: str = "invalid syntax") -> SyntaxError:
    return SyntaxError(f"{error_message}: '{expr}' at line {line}")

def definition_exception(var_name: str, line: int) -> NameError:
    return NameError(f"'{var_name}' isn't defined at line {line}")

def type_exception(var_name: str, expected_type: Type[float | str | bool | list] | str, line: int) -> TypeError:
    type_name: str = "nb" if expected_type == float else ("str" if expected_type == str else ("bool" if expected_type == bool else ("list" if expected_type == list else cast(str, expected_type))))
    return TypeError(f"'{var_name}' isn't a {type_name.replace("|", "or")} at line {line}")

def type_exception_with_value(var_name: str, value, expected_type: Type[float | str | bool | list] | str, line: int) -> TypeError:
    type_name: str = "nb" if expected_type == float else ("str" if expected_type == str else ("bool" if expected_type == bool else ("list" if expected_type == list else cast(str, expected_type))))
    return TypeError(f"'{var_name}' with value {value} isn't a {str(type_name).replace("|", "or")} at line {line}")

def unknown_action_error(action: str, line_nb: int, current_path: str) -> NameError:
    return NameError(f"action {action} unknown at line {line_nb} in {current_path}")

def recursive_file_import_error(path: str, line_nb: int, current_path: str) -> ImportError:
    return ImportError(f"File import from {path} at line {line_nb} in {current_path} is recursive")

def not_in_list_error(value: float | str | bool | list, line_nb: int, current_path: str) -> ValueError:
    return ValueError(f"{value} not in list at line {line_nb} in {current_path}")

def out_of_range_error(line_nb: int, current_path: str) -> IndexError:
    return IndexError(f"index out of range at line {line_nb} in {current_path}")

def keyboard_interrupt(line_nb: int, line: str, current_path: str) -> KeyboardInterrupt:
    return KeyboardInterrupt(f"{line} at line {line_nb} in {current_path}")