"""The module contains constants used in other modules,
such as standard steps for moving worms,
colors for displaying objects on the map, etc."""
from enum import Enum


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


class Neighbors(Enum):
    """Nearest cells for interaction and movement of objects."""
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


class TornadoScatter(Enum):
    """Options for moving objects when hitting the tornado affected area."""
    UP = (0, -5)
    RIGHT = (5, 0)
    DOWN = (0, 5)
    LEFT = (-5, 0)


NEIGHBOURS_VALUES = [Neighbors.UP.value, Neighbors.DOWN.value,
                     Neighbors.LEFT.value, Neighbors.RIGHT.value]

tornado_scatter_values = [TornadoScatter.RIGHT.value, TornadoScatter.LEFT.value,
                          TornadoScatter.DOWN.value, TornadoScatter.UP.value]
