from errors import syntax_exception
from memory_variables import quote_safe_slice, parentheses_extractor, no_space, get_soft_typed_var, get_type


def str_reader(line: str, line_nb: int) -> str:
    while "(" in line:
        line = (
                line[:line.index("(")] + " "
                + str(str_reader(parentheses_extractor(line, line_nb)[0], line_nb))
                + " " + line[parentheses_extractor(line, line_nb)[1] + 1:]
        )

    result = None
    for word in quote_safe_slice(line, "+"):
        if "\"" in word:
            word = " ".join(filter(lambda x: x != "", word.split()))
            if word[0] == "\"":
                if word[-1] == "\"":
                    result = word[1:-1] if result is None else result + word[1:-1]
                else:
                    raise syntax_exception(line, line_nb)
            else:
                raise syntax_exception(line, line_nb)
        else:
            if len(word.split()) != 1:
                raise syntax_exception(line, line_nb)
            value = str(get_soft_typed_var(no_space(word), line_nb))
            if get_type(no_space(word), line_nb) == float:
                if value.split(".")[1] == "0":
                    value = value.split(".")[0]
            result = value if result is None else result + value
    if result is None:
        raise syntax_exception(line, line_nb)
    return result
