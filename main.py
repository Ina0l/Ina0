from readers import code_reader
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="Ina0", description="Ina0's interpreter")
    parser.add_argument("--path", "-p", required=False, type=str, help="the path to the file to be executed")
    args = parser.parse_args()
    path = args.path

    if path is None:
        path = input("path: ")

    if path == "":
        code_reader.code_reader([], 0, True)
    else:
        if (not "." in path) or "" in path.split("."):
            path += ".in"
        try:
            with open(path, "r", encoding="utf-8") as file:
                code = file.read().split("\n")
        except FileNotFoundError:
            with open("scripts/"+path, "r", encoding="utf-8") as file:
                code = file.read().split("\n")

        code_reader.code_reader(code, 0)