from enum import Enum
from collections import namedtuple


class Colors(Enum):
    SPACE = (0, 0, 0)
    FOOD = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (0, 255, 255)
    SKY_BLUE = (235, 206, 135)
    GREY = (72, 72, 72)


Cell = namedtuple('Cell', ['x', 'y'])


class Neighbors(Enum):
    UP = Cell(0, -1)
    RIGHT = Cell(1, 0)
    DOWN = Cell(0, 1)
    LEFT = Cell(-1, 0)


class Tornado_scatter(Enum):
    UP = Cell(0, -5)
    RIGHT = Cell(5, 0)
    DOWN = Cell(0, 5)
    LEFT = Cell(-5, 0)


neighbors_values = [Neighbors.UP.value, Neighbors.DOWN.value, Neighbors.LEFT.value, Neighbors.RIGHT.value]

tornado_scatter_values = [Tornado_scatter.RIGHT.value, Tornado_scatter.LEFT.value, Tornado_scatter.DOWN.value,
                          Tornado_scatter.UP.value]

