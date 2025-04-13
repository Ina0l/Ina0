from typing import List
from random import random

from errors import syntax_exception, definition_exception
from memory_variables import _nb, _str, _bool, _list, _funct, delete_var, set_var, get_var
from readers import nb_reader, str_reader, bool_reader


def code_reader(code: List[str], start_line: int) -> None:
    skip = 0
    opened_if = 0
    opened_while = 0
    line_nb = start_line
    while_loop_code = []
    condition = ""
    funct_def = ""

    for line in code:
        line_nb += 1
        action = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[0]])))

        if action == "enddef":
            funct_def = ""

        if funct_def != "":
            if action == "def": raise syntax_exception(line_nb)
            _funct[funct_def][0].append(line)
            continue

        if action == "endif":
            skip = (skip - 1 if skip != 0 else 0)
            if opened_if == 0: raise syntax_exception(line_nb)
            opened_if -= 1

        if action == "if": opened_if += 1

        if skip > 0: continue

        if action == "endwhile":
            if opened_while == 0: raise syntax_exception(line_nb)
            opened_while -= 1
            if opened_while == 0:
                while _bool[condition]:
                    code_reader(while_loop_code[1:], line_nb - len(while_loop_code))

        if action == "while":
            if opened_while == 0:
                condition = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
                if not condition in _bool: raise definition_exception(condition, line_nb)
            opened_while += 1

        if opened_while > 0:
            while_loop_code.append(line)
            continue

        if action == "nb":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            var_name = line.split("=")[0]
            content = "=".join(line.split("=")[1:])
            delete_var(var_name)
            _nb.update({var_name: nb_reader.nb_reader(content, line_nb)})

        elif action == "str":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))).split("=")[0]
            content = "=".join(line.split("=")[1:])
            delete_var(var_name)
            _str.update({var_name: str_reader.str_reader(content, line_nb)})

        elif action == "bool":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))).split("=")[0]
            content = "=".join(line.split("=")[1:])
            delete_var(var_name)
            _bool.update({var_name: bool_reader.bool_reader(content, line_nb)})

        elif action == "is":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))).split("=")[0]
            content = "=".join(line.split("=")[1:])
            delete_var(var_name)
            _bool.update({var_name: bool_reader.check_reader(content, line_nb)})

        elif action == "if":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line])))
            if not line.split(":")[1] in _bool: raise definition_exception(line.split(":")[1], line_nb)
            if not _bool[line.split(":")[1]]: skip += 1

        elif action == "endif": pass

        elif action == "while":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)

        elif action == "endwhile": pass

        elif action == "def":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            funct_def = "".join(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))
            _funct.update({funct_def: ([], line_nb)})

        elif action == "enddef": pass

        elif action == "in":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            content = input()
            if var_name != "":
                delete_var(var_name)
                _str.update({var_name: content})

        elif action == "len":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))).split("=")[0]
            delete_var(var_name)
            content = get_var("".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]]))).split("=")[1], line_nb)
            if type(content) in (str, list):
                _nb.update({var_name: len(content)})
            else: raise TypeError("variable " + line.split(",")[0] + " isn't a string or list, at line " + str(line_nb))

        elif action == "random":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            var_name = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            delete_var(var_name)
            _bool.update({var_name: random() > 0.5})

        elif action == "out":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            print(str_reader.str_reader(line, line_nb))

        elif action == "del":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            delete_var(line)

        elif action == "lmake":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            delete_var(line)
            _list.update({line: []})

        elif action == "ladd":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            for obj in line.split(",")[1:]:
                _list[line.split(",")[0]].append(get_var(obj, line_nb))

        elif action == "lremove":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            if type(get_var(line.split(",")[0], line_nb)) == list:
                for obj in line.split(",")[1:]:
                    _list[line.split(",")[0]].remove(get_var(obj, line_nb))
            else: raise TypeError("variable " + line.split(",")[0] + " isn't a list at line " + str(line_nb))

        elif action == "lget":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            var_name = line.split("=")[0]
            delete_var(var_name)
            if type(get_var(line.split("=")[1].split(",")[0], line_nb)) == list:
                list_value = _list[line.split("=")[1].split(",")[0]]
            else: raise TypeError("variable " + line.split(",")[0] + " isn't a list at line " + str(line_nb))
            if len(list_value) > nb_reader.nb_reader(line.split("=")[1].split(",")[1], line_nb):
                value = list_value[nb_reader.nb_reader(line.split("=")[1].split(",")[1], line_nb)]
                set_var(var_name, value)
            else: raise IndexError("index out of range at line "+str(line_nb))

        elif action == "lindex":
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            line = "".join(list(filter(lambda x: x != " ", [a for a in line.split(":")[1]])))
            var_name = line.split("=")[0]
            delete_var(var_name)
            list_var = line.split("=")[1].split(",")[0]
            value_var = line.split("=")[1].split(",")[1]
            if type(get_var(list_var, line_nb)) == list:
                if get_var(value_var, line_nb) in get_var(list_var, line_nb):
                    _nb.update({var_name: get_var(list_var, line_nb).index(get_var(value_var, line_nb))})
                else: raise ValueError(str(get_var(value_var, line_nb)) + " not in list at line "+str(line_nb))
            else: raise TypeError("variable "+str(list_var)+" isn't a list at line "+str(line_nb))

        elif action in _funct:
            if len(line.split(":")) != 2: raise syntax_exception(line_nb)
            function = _funct[action]
            code_reader(function[0], function[1])

        elif action == "" and not ":" in line: pass
        else:
            raise NameError("action " + action + " unknown")
    if opened_if != 0: raise syntax_exception(len(code))
    if opened_while != 0: raise syntax_exception(len(code))