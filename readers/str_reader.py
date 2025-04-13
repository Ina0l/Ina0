from errors import syntax_exception
from memory_variables import get_var


def str_reader(code_line: str, line: int) -> str:
    words=[]
    quote_open = False
    word = ""
    for char in code_line:
        if char == "\"" and not quote_open:
            if word!="": words.append(word)
            quote_open, word = True, "\""
            continue
        word+=char
        if char == "\"" and quote_open:
            words.append(word)
            quote_open, word = False, ""
    if word != "": words.append(word)
    if quote_open:
        raise syntax_exception(line)

    code = ""
    for word in words:
        if word[0]=="\"": code+=word[1:-1]
        else:
            for member in word.split(" "):
                if member!="": code += str(get_var(member, line))
    return code
