from readers import code_reader
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=False, type=str)
    args = parser.parse_args()
    path = args.path

    if path is None:
        path = input("path: ")

    if path[-3:] != ".in": path += ".in"

    try:
        with open(path, "r", encoding="utf-8") as file:
            code = file.read().split("\n")
    except FileNotFoundError:
        with open("scripts/"+path, "r", encoding="utf-8") as file:
            code = file.read().split("\n")

    code_reader.code_reader(code, 0)