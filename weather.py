import random
from common_types import Cell, Neighbors_values
from operator import add
from worm import Worm, Food


class Weather_Event:
    def __init__(self, start_coordinates: tuple):
        self._zero_coordinates = start_coordinates


class Rain(Weather_Event):
    def __init__(self, start_coordinates: tuple):
        super().__init__(start_coordinates)
        self._side: int = random.randrange(2, 5)
        self._duration: int = random.randrange(3, 10)
        self._all_coordinates: list = []

    def describe(self):
        print('start coordinates:', self._zero_coordinates)
        print('side:', self._side)
        print('duration:', self._duration)
        print('all', self._all_coordinates)

    def upscaling(self, border_x: int, border_y: int) -> None:
        coordinates = []
        step_forward = (1, 0)
        step_down = (0, 1)
        line_begin_coordinates = self._zero_coordinates
        for i in range(self._side):
            line_coordinates = []
            for n in range(self._side):
                if n == 0:
                    last_coordinates = None
                else:
                    last_coordinates = line_coordinates.pop()
                    line_coordinates.append(last_coordinates)

                if last_coordinates is None:
                    line_coordinates.append(line_begin_coordinates)
                else:
                    next_coordinates_raw = tuple(map(add, step_forward, last_coordinates))
                    next_x = min(max(next_coordinates_raw[0], 0), border_x - 1)
                    next_y = min(max(next_coordinates_raw[1], 0), border_y - 1)
                    next_coordinates = Cell(next_x, next_y)
                    if next_coordinates not in line_coordinates:
                        line_coordinates.append(next_coordinates)
            coordinates.extend(line_coordinates)
            line_begin_coordinates_raw = tuple(map(add, step_down, line_begin_coordinates))
            line_begin_coordinates = Cell(line_begin_coordinates_raw[0], line_begin_coordinates_raw[1])
        self._all_coordinates = coordinates

    @property
    def coordinates(self):
        return self._zero_coordinates

    def decrease_duration(self) -> None:
        self._duration -= 1

    @property
    def is_over(self) -> int:
        return self._duration <= 0

    @property
    def all_coordinates(self) -> list:
        return self._all_coordinates

    def move(self, border_x: int, border_y: int) -> None:
        if not self.is_over:
            step = random.choice(Neighbors_values)
            new_coordinates = tuple(map(add, step, self._zero_coordinates))
            new_x = min(max(new_coordinates[0], 0), border_x - 1)
            new_y = min(max(new_coordinates[1], 0), border_y - 1)
            self._zero_coordinates = Cell(new_x, new_y)

    def raining_effect(self, affected_worms: list[Worm], affected_food: list[Food]) -> None:
        if len(affected_worms) > 0:
            for worm in affected_worms:
                worm.health -= 0.2
                worm.damage -= 0.1

        if len(affected_food) > 0:
            for item in affected_food:
                item.nutritional_value -= 0.5


if __name__ == "__main__":
    width = 100
    height = 100
    rain = Rain(Cell(random.randrange(0, width), random.randrange(0, height)))
    rain.describe()
    rain.move(width, height)
    rain.upscaling(width, height)
    rain.describe()
