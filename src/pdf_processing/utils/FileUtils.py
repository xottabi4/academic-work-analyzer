def readTextFileLines(path):
    with open(path) as f:
        lines = f.read().splitlines()
        return lines
