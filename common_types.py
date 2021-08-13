from enum import Enum
from collections import namedtuple


class Colors(Enum):
    SPACE = (0, 0, 0)
    FOOD = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (0, 255, 255)


Cell = namedtuple('Cell', ['x', 'y'])


class Neighbors(Enum):
    UP = Cell(0, -1)
    RIGHT = Cell(1, 0)
    DOWN = Cell(0, 1)
    LEFT = Cell(-1, 0)



