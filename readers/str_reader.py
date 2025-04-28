from errors import syntax_exception
from memory_variables import get_var, slice_quote_apart, parentheses_extractor, no_space


def str_reader(line: str, line_nb: int) -> str:
    while "(" in line:
        line = (line[:line.index("(")] + " " +
                     str(str_reader(parentheses_extractor(line, line_nb)[0], line_nb)) +
                     " " + line[parentheses_extractor(line, line_nb)[1] + 1:])

    result = None
    for word in slice_quote_apart(line, "+"):
        if "\"" in word:
            word = " ".join(filter(lambda x: x != "", word.split()))
            if word[0] == "\"":
                if word[-1] == "\"":
                    result = word[1:-1] if result is None else result + word[1:-1]
                else: raise syntax_exception(line_nb)
            else: raise syntax_exception(line_nb)
        else:
            if len(word.split()) != 1: raise syntax_exception(line_nb)
            result = str(get_var(no_space(word), line_nb)) if result is None else result + str(get_var(no_space(word), line_nb))
    if result is None: raise syntax_exception(line_nb)
    return result
