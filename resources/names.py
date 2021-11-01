from typing import List
import os


def __read_names(filename) -> List[str]:
    """Creates pool of names from an external file."""
    names = []
    with open(filename, 'r', encoding=None) as reader:
        for line in reader:
            names.append(line.rstrip('\n'))
    return names


__NAMES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'names.txt')
NAMES = __read_names(__NAMES_PATH)
