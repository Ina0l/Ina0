def syntax_exception(line: int) -> SyntaxError:
    return SyntaxError("invalid syntax at line "+str(line))

def definition_exception(var_name: str, line: int) -> NameError:
    return NameError(var_name+ " isn't defined at line "+str(line))
