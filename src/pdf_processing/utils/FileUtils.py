def readTextFileLines(path):
    with open(path) as f:
        lines = f.read().splitlines()
        return lines


def saveContentToFile(stringContent, output_filename):
    with open(output_filename, mode='w') as fout:
        fout.write(stringContent)
