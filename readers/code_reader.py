from typing import List, Union, Tuple, Optional
from random import getrandbits
from math import floor

from errors import syntax_exception, type_exception, definition_exception
from memory_variables import _funct, delete_var, set_var, get_var, delete_other_instance, \
    get_type, no_space, quote_safe_slice, get_soft_typed_var, quote_safe_no_space, _nb, _str
from readers import nb_reader, str_reader, bool_reader


def code_reader(code: List[str], start_line: int, terminal_mode=False) -> Optional[Tuple[
        Union[float, str, bool, list, None],
        List[Tuple[str, Union[float, str, bool, list, None]]]
    ]]:
    skip = 0
    opened_if = 0
    opened_while = 0
    line_nb = start_line
    while_loop_code = []
    condition = ""
    funct_def = ""
    locally_set_var: List[Tuple[str, Union[float, str, bool, list, None]]] = []
    line_index = 0
    while line_index < len(code) or terminal_mode:
        if terminal_mode:
            line = input(">>> ")
        else:
            line = code[line_index]
            line_index += 1

        if "//" in line:
            line = quote_safe_slice(line, "//")[0]

        line_nb += 1
        action = no_space(quote_safe_slice(line, ":")[0])

        if action == "quit":
            terminal_mode = False
            line_index = len(code)

        if action == "end_def":
            funct_def = ""

        if funct_def != "":
            if action == "def":
                raise syntax_exception(action, line_nb)
            _funct[funct_def][0].append(line)
            continue

        if action == "end_if":
            if not opened_while > 0:
                skip = (skip - 1 if skip != 0 else 0)
                if opened_if == 0:
                    raise syntax_exception(action, line_nb)
                opened_if -= 1

        if action == "end_while":
            if not skip > 0:
                if opened_while == 0:
                    raise syntax_exception(action, line_nb)
                opened_while -= 1
                if opened_while == 0:
                    while bool_reader.bool_reader(condition, line_nb):
                        code_reader(while_loop_code[1:], line_nb - len(while_loop_code))
                    while_loop_code = []

        if action == "if":
            if not opened_while > 0:
                opened_if += 1
                if not bool_reader.bool_reader(quote_safe_slice(line, ":")[1], line_nb):
                    skip += 1

        if action == "while":
            if not skip > 0:
                if opened_while == 0:
                    condition = quote_safe_slice(line, ":")[1]
                    bool_reader.bool_reader(condition, line_nb)
                opened_while += 1

        if skip > 0:
            continue

        if opened_while > 0:
            while_loop_code.append(line)
            continue

        if action == "nb":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            line = no_space(quote_safe_slice(line, ":")[1])
            var_name = quote_safe_slice(line, "=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = quote_safe_slice(line, "=")[1]
            set_var(var_name, nb_reader.nb_reader(content, line_nb))
            delete_other_instance(var_name, float)

        elif action == "str":
            var_name = no_space(quote_safe_slice(line, ":")[1].split("=")[0])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = quote_safe_slice(line, "=")[1]
            set_var(var_name, str_reader.str_reader(content, line_nb))
            delete_other_instance(var_name, str)

        elif action == "bool":
            var_name = no_space(quote_safe_slice(line, ":")[1].split("=")[0])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = "=".join(quote_safe_slice(line, "=")[1:])
            set_var(var_name, bool_reader.bool_reader(content, line_nb))
            delete_other_instance(var_name, bool)

        elif action == "if":
            pass

        elif action == "end_if":
            pass

        elif action == "while":
            pass

        elif action == "end_while":
            pass

        elif action == "def":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            if len(quote_safe_slice(line, "<-")) > 2:
                raise syntax_exception(line, line_nb)
            funct_def = no_space(quote_safe_slice(line, ":")[1].split("<-")[0])
            if "<-" in line:
                funct_parameters = tuple(no_space(a) for a in quote_safe_slice(quote_safe_slice(line, "<-")[-1], ","))
            else:
                funct_parameters = ()
            _funct.update({funct_def: ([], funct_parameters, line_nb)})

        elif action == "end_def":
            pass

        elif action == "return":
            if start_line == 0:
                raise syntax_exception(action, line_nb)
            code = quote_safe_slice(line, ":")[1]
            if get_type(code, line_nb) == float:
                return nb_reader.nb_reader(no_space(code), line_nb), locally_set_var
            elif get_type(code, line_nb) == str:
                return str_reader.str_reader(code, line_nb), locally_set_var
            elif get_type(code, line_nb) == bool:
                return bool_reader.bool_reader(code, line_nb), locally_set_var
            elif get_type(code, line_nb) == list:
                return get_var(no_space(code), line_nb, list), locally_set_var
            else:
                raise definition_exception(code, line_nb)

        elif action == "input":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            var_name = no_space(quote_safe_slice(line, ":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = input()
            if var_name != "":
                delete_var(var_name)
                set_var(var_name, content)

        elif action == "len":
            var_name = no_space(quote_safe_slice(line, ":")[1]).split("<-")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = quote_safe_slice(quote_safe_slice(line, ":")[1], "<-")[1]
            if get_type(content, line_nb) == str:
                set_var(var_name, float(len(str_reader.str_reader(content, line_nb))))
                delete_other_instance(var_name, float)
            elif get_type(no_space(content), line_nb) == list:
                set_var(var_name, float(len(get_var(no_space(content), line_nb, list))))
                delete_other_instance(var_name, float)
            else:
                raise type_exception(quote_safe_slice(line, "<-")[0], "string or list", line_nb)

        elif action == "round":
            if len(quote_safe_slice(line, ":")) != 2 or len(quote_safe_slice(line, "=")) != 2:
                raise syntax_exception(line, line_nb)
            var_name = no_space(quote_safe_slice(line, ":")[1]).split("=")[0]
            content = nb_reader.nb_reader(no_space(quote_safe_slice(line, ":")[1]).split("=")[1], line_nb)
            set_var(var_name, content)
            delete_other_instance(var_name, float)

        elif action == "random":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            var_name = no_space(quote_safe_slice(line, ":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            delete_var(var_name)
            set_var(var_name, bool(getrandbits(1)))

        elif action == "out":
            if ":" in line:
                print(str_reader.str_reader(quote_safe_slice(line, ":")[1], line_nb))
            else:
                print()

        elif action == "del":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            for var_name in no_space(quote_safe_slice(line, ":")[1]).split(","):
                delete_var(var_name)

        elif action == "make_list":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            var_name = no_space(quote_safe_slice(line, ":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            delete_var(var_name)
            set_var(var_name, [])

        elif action == "append":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            if len(quote_safe_slice(line, "<-")) != 2:
                raise syntax_exception(line, line_nb)
            line = quote_safe_slice(line, ":")[1]
            parameters = quote_safe_slice(quote_safe_slice(line, "<-")[1], ",")
            if get_type(parameters[0], line_nb) != list:
                raise type_exception(no_space(parameters[0]), list, line_nb)
            for obj in parameters[1:]:
                if get_type(obj, line_nb) == float:
                    value = nb_reader.nb_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == str:
                    value = str_reader.str_reader(obj, line_nb)
                elif get_type(obj, line_nb) == bool:
                    value = bool_reader.bool_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == list:
                    value = get_var(no_space(obj), line_nb, list)
                else:
                    raise definition_exception(obj, line_nb)
                get_var(no_space(parameters[0]), line_nb, list).append(value)

        elif action == "remove":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            if len(quote_safe_slice(line, "<-")) != 2:
                raise syntax_exception(line, line_nb)
            line = quote_safe_slice(line, ":")[1]

            parameters = quote_safe_slice(quote_safe_no_space(quote_safe_slice(line, "<-")[1]), ",")
            if get_type(parameters[0], line_nb) != list:
                raise type_exception(parameters[0], list, line_nb)
            for obj in parameters[1:]:
                if get_type(obj, line_nb) == float:
                    value = nb_reader.nb_reader(obj, line_nb)
                elif get_type(obj, line_nb) == str:
                    value = str_reader.str_reader(obj, line_nb)
                elif get_type(obj, line_nb) == bool:
                    value = bool_reader.bool_reader(obj, line_nb)
                elif get_type(obj, line_nb) == list:
                    value = get_var(obj, line_nb, list)
                else:
                    raise definition_exception(obj, line_nb)
                called_list = get_var(parameters[0], line_nb, list)
                if value in called_list:
                    called_list.remove(value)
                else:
                    raise ValueError(parameters[0] + " not in list at line " + str(line_nb))

        elif action == "get":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            line = no_space(quote_safe_slice(line, ":")[1])
            var_name = quote_safe_slice(line, "<-")[0]
            parameters = quote_safe_slice(quote_safe_no_space(quote_safe_slice(line, "<-")[1]), ",")
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            if get_type(parameters[0], line_nb) == list:
                origin_value = get_var(parameters[0], line_nb, list)
            elif get_type(parameters[0], line_nb) == str:
                origin_value = str_reader.str_reader(parameters[0], line_nb)
            else:
                raise type_exception(parameters[0], "list or string", line_nb)
            if len(origin_value) > nb_reader.nb_reader(parameters[1], line_nb):
                value = origin_value[floor(nb_reader.nb_reader(parameters[1], line_nb))]
                set_var(var_name, value)
                delete_other_instance(var_name, type(value))
            else:
                raise IndexError("index out of range at line "+str(line_nb))

        elif action == "set":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            line = quote_safe_slice(line, ":")[1]
            parameters = quote_safe_slice(quote_safe_no_space(quote_safe_slice(line, "<-")[1]), ",")
            list_var = get_var(parameters[0], line_nb, list)
            index = nb_reader.nb_reader(no_space(parameters[1]), line_nb)
            if not 0 <= index < len(list_var):
                raise IndexError("index out of range at line " + str(line_nb))

            if get_type(parameters[2], line_nb) == float:
                value = nb_reader.nb_reader(no_space(parameters[2]), line_nb)
            elif get_type(parameters[2], line_nb) == str:
                value = str_reader.str_reader(parameters[2], line_nb)
            elif get_type(parameters[2], line_nb) == bool:
                value = bool_reader.bool_reader(parameters[2], line_nb)
            elif get_type(parameters[2], line_nb) == list:
                value = get_var(no_space(parameters[2]), line_nb, list)
            else:
                raise syntax_exception(parameters[2], line_nb)

            list_var[floor(index)] = value

        elif action == "index":
            if len(quote_safe_slice(line, ":")) != 2:
                raise syntax_exception(line, line_nb)
            line = no_space(quote_safe_slice(line, ":")[1])
            var_name = quote_safe_slice(line, "<-")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_soft_typed_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            iterable_var = quote_safe_slice(quote_safe_slice(line, "<-")[1], ",")[0]
            value_var = quote_safe_slice(quote_safe_slice(line, "<-")[1], ",")[1]
            if get_type(iterable_var, line_nb) in (list, str):
                if get_type(value_var, line_nb) == float:
                    value = nb_reader.nb_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == str:
                    value = str_reader.str_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == bool:
                    value = bool_reader.bool_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == list:
                    value = get_var(value_var, line_nb, list)
                else:
                    raise syntax_exception(value_var, line_nb)
                if value in get_var(iterable_var, line_nb, Union[list, str]):
                    set_var(var_name, float(get_var(iterable_var, line_nb, Union[list, str]).index(value)))
                    delete_other_instance(var_name, float)
                else:
                    raise ValueError(str(get_var(value_var, line_nb, Union[list, str])) + " not in list at line " + str(line_nb))
            else:
                raise type_exception(iterable_var, list, line_nb)

        elif action in _funct:
            if ":" in line:
                var_name = no_space(quote_safe_slice(line, ":")[1].split("<-")[0])
                if "<-" in line:
                    params_values = quote_safe_slice(quote_safe_slice(line, "<-")[1], ",")
                else:
                    params_values = []
            else:
                params_values, var_name = [], None
            function = _funct[action]
            if len(params_values) != len(function[1]):
                raise syntax_exception(line, line_nb)
            outside_params = {}
            for param_index in range(len(function[1])):
                parameter_name = function[1][param_index]
                try:
                    outside_params.update({parameter_name: get_soft_typed_var(parameter_name, line_nb)})
                except NameError:
                    pass
                if get_type(no_space(params_values[param_index]), line_nb) == float:
                    set_var(parameter_name, nb_reader.nb_reader(no_space(params_values[param_index]), line_nb))
                    delete_other_instance(parameter_name, float)
                elif get_type(params_values[param_index], line_nb) == str:
                    set_var(parameter_name, str_reader.str_reader(params_values[param_index], line_nb))
                    delete_other_instance(parameter_name, str)
                elif get_type(params_values[param_index], line_nb) == bool:
                    set_var(parameter_name, bool_reader.bool_reader(params_values[param_index], line_nb))
                    delete_other_instance(parameter_name, bool)
                elif get_type(params_values[param_index], line_nb) == list:
                    set_var(parameter_name, get_var(no_space(params_values[param_index]), line_nb, list))
                    delete_other_instance(parameter_name, list)

            callback = code_reader(function[0], function[2])
            assert callback is not None

            for var in callback[1]:
                delete_var(var[0])
                value_var = var[1]
                if value_var is not None:
                    set_var(var[0], value_var)
                else:
                    delete_var(var[0])
            for param_index in range(len(function[1])):
                delete_var(function[1][param_index])
                if function[1][param_index] in outside_params:
                    set_var(function[1][param_index], outside_params[function[1][param_index]])
            result = callback[0]
            if result is not None:
                if ":" in line:
                    assert var_name is not None
                    delete_var(var_name)
                    set_var(var_name, result)

        elif action == "" and not ":" in line:
            pass
        else:
            raise NameError("action " + action + " unknown")
    if opened_if != 0:
        raise syntax_exception("", len(code))
    if opened_while != 0:
        raise syntax_exception("", len(code))
    return None, locally_set_var