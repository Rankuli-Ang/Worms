"""The module contains constants used in other modules,
such as standard steps for moving worms,
colors for displaying objects on the map, etc."""
from enum import Enum
from collections import namedtuple


class Colors(Enum):
    """Displayed colors of objects on the map."""
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
    """Nearest cells for interaction and movement of objects."""
    UP = Cell(0, -1)
    RIGHT = Cell(1, 0)
    DOWN = Cell(0, 1)
    LEFT = Cell(-1, 0)


class TornadoScatter(Enum):
    """Options for moving objects when hitting the tornado affected area."""
    UP = Cell(0, -5)
    RIGHT = Cell(5, 0)
    DOWN = Cell(0, 5)
    LEFT = Cell(-5, 0)


NEIGHBOURS_VALUES = [Neighbors.UP.value, Neighbors.DOWN.value,
                     Neighbors.LEFT.value, Neighbors.RIGHT.value]

tornado_scatter_values = [TornadoScatter.RIGHT.value, TornadoScatter.LEFT.value,
                          TornadoScatter.DOWN.value, TornadoScatter.UP.value]


# c1, c2 = Cell(10, 10), Cell(20, 20)
# p1, p2 = (10, 10), (20, 20)
# iters = 100000
