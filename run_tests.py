from os import listdir
from os.path import isfile, join

from readers import code_reader


if __name__ == "__main__":
    paths = []
    directories = ["scripts\\tests"]
    while len(directories) != 0:
        for path in listdir(directories[0]):
            if isfile(join(directories[0], path)): paths.append(join(directories[0], path))
            else:
                directories.append(join(directories[0], path))
        directories = directories[1:]

    for path in paths:
        print(path)
        print()
        with open(path, "r", encoding="utf-8") as file:
            code = file.read().split("\n")
        code_reader.code_reader(code, 0)
        print("\n\n")