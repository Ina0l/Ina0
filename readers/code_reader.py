from typing import List, Union, Tuple
from random import random
from math import floor

from errors import syntax_exception, type_exception, definition_exception
from memory_variables import _nb, _str, _bool, _list, _funct, delete_var, set_var, get_var, delete_other_instance, \
    get_type, no_space
from readers import nb_reader, str_reader, bool_reader


def code_reader(code: List[str], start_line: int) -> Tuple[Union[float, str, bool, list, None], List[Tuple[str, Union[float, str, bool, list, None]]]]:
    skip = 0
    opened_if = 0
    opened_while = 0
    line_nb = start_line
    while_loop_code = []
    condition = ""
    funct_def = ""
    locally_set_var: List[Tuple[str, Union[float, str, bool, list, None]]] = []

    for line in code:

        if "//" in line:
            line = line.split("//")[0]

        line_nb += 1
        action = no_space(line.split(":")[0])

        if action == "enddef":
            funct_def = ""

        if funct_def != "":
            if action == "def": raise syntax_exception(line_nb)
            _funct[funct_def][0].append(line)
            continue

        if action == "endif":
            if not opened_while > 0:
                skip = (skip - 1 if skip != 0 else 0)
                if opened_if == 0: raise syntax_exception(line_nb)
                opened_if -= 1

        if action == "endwhile":
            if not skip > 0:
                if opened_while == 0: raise syntax_exception(line_nb)
                opened_while -= 1
                if opened_while == 0:
                    while bool_reader.bool_reader(condition, line_nb):
                        code_reader(while_loop_code[1:], line_nb - len(while_loop_code))
                    while_loop_code = []

        if action == "if":
            if not opened_while > 0:
                opened_if += 1
                if not bool_reader.bool_reader(line.split(":")[1], line_nb): skip += 1

        if action == "while":
            if not skip > 0:
                if opened_while == 0:
                    condition = line.split(":")[1]
                    bool_reader.bool_reader(condition, line_nb)
                opened_while += 1

        if skip > 0: continue

        if opened_while > 0:
            while_loop_code.append(line)
            continue

        if action == "nb":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = no_space(line.split(":")[1])
            var_name = line.split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = "=".join(line.split("=")[1:])
            _nb.update({var_name: nb_reader.nb_reader(content, line_nb)})
            delete_other_instance(var_name, float)

        elif action == "str":
            var_name = no_space(":".join(line.split(":")[1:])).split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = "=".join(line.split("=")[1:])
            _str.update({var_name: str_reader.str_reader(content, line_nb)})
            delete_other_instance(var_name, str)

        elif action == "bool":
            var_name = no_space(":".join(line.split(":")[1:])).split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = "=".join(line.split("=")[1:])
            _bool.update({var_name: bool_reader.bool_reader(content, line_nb)})
            delete_other_instance(var_name, bool)

        elif action == "if": pass

        elif action == "endif": pass

        elif action == "while": pass

        elif action == "endwhile": pass

        elif action == "def":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            if len(line.split("<-")) > 2: raise syntax_exception(line_nb)
            funct_def = no_space(line.split(":")[1].split("<-")[0])
            if "<-" in line:
                funct_parameters = tuple(no_space(a) for a in line.split("<-")[-1].split(","))
            else: funct_parameters = ()
            _funct.update({funct_def: ([], funct_parameters, line_nb)})

        elif action == "enddef": pass

        elif action == "return":
            if start_line == 0: raise syntax_exception(line_nb)
            code = ":".join(line.split(":")[1:])
            if get_type(code, line_nb) == float:
                return nb_reader.nb_reader(no_space(code), line_nb), locally_set_var
            elif get_type(code, line_nb) == str:
                return str_reader.str_reader(code, line_nb), locally_set_var
            elif get_type(code, line_nb) == bool:
                return bool_reader.bool_reader(code, line_nb), locally_set_var
            elif get_type(code, line_nb) == list:
                return get_var(no_space(code), line_nb), locally_set_var
            else: raise definition_exception(code, line_nb)

        elif action == "input":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = no_space(line.split(":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = input()
            if var_name != "":
                delete_var(var_name)
                _str.update({var_name: content})

        elif action == "len":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = no_space(":".join(line.split(":")[1:])).split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            content = no_space(":".join(line.split(":")[1:])).split("=")[1]
            if get_type(content, line_nb) == str:
                _nb.update({var_name: len(str_reader.str_reader(content, line_nb))})
                delete_other_instance(var_name, float)
            elif get_type(content, line_nb) == list:
                _nb.update({var_name: len(get_var(content, line_nb))})
                delete_other_instance(var_name, float)
            else: raise type_exception(line.split(",")[0], "string or list", line_nb)

        elif action == "random":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = no_space(line.split(":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            delete_var(var_name)
            _bool.update({var_name: random() > 0.5})

        elif action == "out":
            print(str_reader.str_reader(":".join(line.split(":")[1:]), line_nb))

        elif action == "del":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            for var_name in no_space(line.split(":")[1]).split(","):
                delete_var(var_name)

        elif action == "lmake":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = no_space(line.split(":")[1])
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            delete_var(var_name)
            _list.update({var_name: []})

        elif action == "ladd":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            if len(line.split("<-")) < 2: raise syntax_exception(line_nb)
            line = ":".join(line.split(":")[1:])
            if get_type(line.split("<-")[0], line_nb) != list:
                raise type_exception(no_space(line.split("<-")[0]), list, line_nb)
            for obj in "<-".join(line.split("<-")[1:]).split(","):
                if get_type(obj, line_nb) == float:
                    value = nb_reader.nb_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == str:
                    value = str_reader.str_reader(obj, line_nb)
                elif get_type(obj, line_nb) == bool:
                    value = bool_reader.bool_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == list:
                    value = get_var(no_space(obj), line_nb)
                else: raise definition_exception(obj, line_nb)
                _list[no_space(line.split("<-")[0])].append(value)

        elif action == "lremove":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            if len(line.split("<-")) < 2: raise syntax_exception(line_nb)
            line = ":".join(line.split(":")[1:])
            if get_type(line.split("<-")[0], line_nb) != list:
                raise type_exception(no_space(line.split("<-")[0]), list, line_nb)
            for obj in "<-".join(line.split("<-")[1:]).split(","):
                if get_type("".join(filter(lambda x: x!=" ", [a for a in obj])), line_nb) == float:
                    value = nb_reader.nb_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == str:
                    value = str_reader.str_reader(obj, line_nb)
                elif get_type(obj, line_nb) == bool:
                    value = bool_reader.bool_reader(no_space(obj), line_nb)
                elif get_type(obj, line_nb) == list:
                    value = get_var(no_space(obj), line_nb)
                else: raise definition_exception(obj, line_nb)
                if value in _list[no_space(line.split("<-")[0])]:
                    _list[no_space(line.split("<-")[0])].remove(value)
                else: raise ValueError(no_space(line.split("<-")[0]) + " not in list at line "+str(line_nb))

        elif action == "lget":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = no_space(line.split(":")[1])
            var_name = line.split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            if type(get_var(line.split("=")[1].split("<-")[0], line_nb)) == list:
                list_value = _list[line.split("=")[1].split("<-")[0]]
            else: raise type_exception(line.split("<-")[0], list, line_nb)
            if len(list_value) > nb_reader.nb_reader(line.split("=")[1].split("<-")[1], line_nb):
                value = list_value[floor(nb_reader.nb_reader(line.split("=")[1].split("<-")[1], line_nb))]
                set_var(var_name, value)
                delete_other_instance(var_name, type(value))
            else: raise IndexError("index out of range at line "+str(line_nb))

        elif action == "lset":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = line.split(":")[1]
            list_var_name = no_space(line.split("=")[0].split("<-")[0])
            if list_var_name in _list: list_var = get_var(list_var_name, line_nb)
            else:
                get_var(list_var_name, line_nb)
                raise type_exception(list_var_name, list, line_nb)
            index = nb_reader.nb_reader(no_space(line.split("=")[0].split("<-")[1]), line_nb)
            if not 0 <= index < len(list_var): raise IndexError("index out of range at line "+str(line_nb))

            value_var = line.split("=")[1]
            if get_type(value_var, line_nb) == float:
                value = nb_reader.nb_reader(no_space(value_var), line_nb)
            elif get_type(value_var, line_nb) == str:
                value = str_reader.str_reader(value_var, line_nb)
            elif get_type(value_var, line_nb) == bool:
                value = bool_reader.bool_reader(value_var, line_nb)
            elif get_type(value_var, line_nb) == list:
                value = get_var(no_space(value_var), line_nb)
            else: raise syntax_exception(line_nb)

            list_var[floor(index)] = value

        elif action == "lindex":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            var_name = line.split("=")[0]
            if not var_name in [a[0] for a in locally_set_var]:
                try:
                    locally_set_var.append((var_name, get_var(var_name, line_nb)))
                except NameError:
                    locally_set_var.append((var_name, None))
            list_var = line.split("=")[1].split("<-")[0]
            value_var = line.split("=")[1].split("<-")[1]
            if type(get_var(list_var, line_nb)) == list:
                if get_type(value_var, line_nb) == float:
                    value = nb_reader.nb_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == str:
                    value = str_reader.str_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == bool:
                    value = bool_reader.bool_reader(value_var, line_nb)
                elif get_type(value_var, line_nb) == list:
                    value = get_var(value_var, line_nb)
                else: raise syntax_exception(line_nb)
                if value in get_var(list_var, line_nb):
                    _nb.update({var_name: get_var(list_var, line_nb).index(value)})
                    delete_other_instance(var_name, float)
                else: raise ValueError(str(get_var(value_var, line_nb)) + " not in list at line "+str(line_nb))
            else: raise type_exception(list_var, list, line_nb)

        elif action in _funct:
            if ":" in line:
                var_name = no_space(line.split(":")[1].split("<-")[0])
                params_values = list(filter(lambda x: x!="", "".join(line.split("<-")[1:]).split(",")))
            else: params_values, var_name = [], None
            function = _funct[action]
            if len(params_values) != len(function[1]): raise syntax_exception(line_nb)
            outside_params = {}
            for param_index in range(len(function[1])):
                try:
                    outside_params.update({function[1][param_index]: get_var(function[1][param_index], line_nb)})
                except NameError: pass
                if get_type(no_space(params_values[param_index]), line_nb) == float:
                    _nb.update({function[1][param_index]: nb_reader.nb_reader(no_space(params_values[param_index]), line_nb)})
                    delete_other_instance(function[1][param_index], float)
                elif get_type(params_values[param_index], line_nb) == str:
                    _str.update({function[1][param_index]: str_reader.str_reader(params_values[param_index], line_nb)})
                    delete_other_instance(function[1][param_index], str)
                elif get_type(params_values[param_index], line_nb) == bool:
                    _bool.update({function[1][param_index]: bool_reader.bool_reader(params_values[param_index], line_nb)})
                    delete_other_instance(function[1][param_index], bool)
                elif get_type(params_values[param_index], line_nb) == list:
                    _list.update({function[1][param_index]: get_var(no_space(params_values[param_index]), line_nb)})
                    delete_other_instance(function[1][param_index], list)

            callback = code_reader(function[0], function[2])

            for var in callback[1]:
                delete_var(var[0])
                if not var[1] is None:
                    set_var(var[0], var[1])
                else: delete_var(var[0])
            for param_index in range(len(function[1])):
                delete_var(function[1][param_index])
                if function[1][param_index] in outside_params:
                    set_var(function[1][param_index], outside_params[function[1][param_index]])
            if not callback[0] is None:
                if ":" in line: set_var(var_name, callback[0])

        elif action == "" and not ":" in line: pass
        else: raise NameError("action " + action + " unknown")
    if opened_if != 0: raise syntax_exception(len(code))
    if opened_while != 0: raise syntax_exception(len(code))
    return None, locally_set_var