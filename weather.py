from typing import List

import random
from common_types import Cell, NEIGHBOURS_VALUES, tornado_scatter_values
from operator import add
from worm import Worm, Food


class WeatherEvent:
    """skeleton class for weather objects on the map"""
    def __init__(self, start_coordinates: tuple):
        self._zero_coordinates = start_coordinates
        self._side: int = 0
        self._duration: int = 0
        self._all_coordinates: List = []

    def upscaling(self, border_x: int, border_y: int) -> None:
        """creates a list of coordinates according to the size of the weather object """
        coordinates = []
        step_forward = (1, 0)
        step_down = (0, 1)
        line_begin_coordinates = self._zero_coordinates
        for i in range(self._side):
            line_coordinates = []
            for ii in range(self._side):
                if ii == 0:
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
            line_begin_coordinates = Cell(line_begin_coordinates_raw[0],
                                          min(max(line_begin_coordinates_raw[1], 0), border_y - 1))
        self._all_coordinates = coordinates

    @property
    def duration(self):
        return self._duration

    @property
    def coordinates(self):
        return self._zero_coordinates

    def decrease_duration(self) -> None:
        self._duration -= 1

    @property
    def is_over(self) -> bool:
        return self._duration <= 0

    @property
    def all_coordinates(self) -> List:
        return self._all_coordinates

    def move(self, border_x: int, border_y: int) -> None:
        if not self.is_over:
            self.decrease_duration()
            step = random.choice(NEIGHBOURS_VALUES)
            new_coordinates = tuple(map(add, step, self._zero_coordinates))
            new_x = min(max(new_coordinates[0], 0), border_x - 1)
            new_y = min(max(new_coordinates[1], 0), border_y - 1)
            self._zero_coordinates = Cell(new_x, new_y)


class Rain(WeatherEvent):
    """an object on the map that occupies a certain area that reduces the health and damage of worms """
    def __init__(self, start_coordinates: tuple):
        super().__init__(start_coordinates)
        self._side: int = random.randrange(3, 8)
        self._duration: int = random.randrange(20, 50)
        self._all_coordinates: List = []

    @staticmethod
    def raining_effect(self, affected_worms: List[Worm], affected_food: List[Food]) -> None:
        """the effect of reducing the characteristics of worms caught in the affected area """
        if len(affected_worms) > 0:
            for worm in affected_worms:
                worm.health -= 0.2
                worm.damage -= 0.1

        if len(affected_food) > 0:
            for item in affected_food:
                item.nutritional_value -= 0.5


class Tornado(WeatherEvent):
    """an object on the map scattering other objects 5 cells to the sides """
    def __init__(self, start_coordinates: tuple):
        super().__init__(start_coordinates)
        self._side: int = random.randrange(3, 8)
        self._duration: int = random.randrange(60, 100)
        self._all_coordinates: List = []
        self._charge: int = 20
        self._direction = random.choice(NEIGHBOURS_VALUES)

    @staticmethod
    def tornado_effect(self, affected_worms: List[Worm],
                       affected_food: List[Food], border_x: int, border_y: int):
        """scattering objects in the affected area """
        if len(affected_worms) > 0:
            for worm in affected_worms:
                throw = random.choice(tornado_scatter_values)
                worm.move(throw, border_x, border_y)

        if len(affected_food) > 0:
            for food in affected_food:
                throw = random.choice(tornado_scatter_values)
                food.relocation(throw, border_x, border_y)

    def move(self, border_x: int, border_y: int) -> None:
        if not self.is_over:
            self.decrease_duration()
            if self._charge <= 0:
                self._direction = random.choice(NEIGHBOURS_VALUES)
                self._charge = 10
            self._charge -= 1
            new_coordinates = tuple(map(add, self._direction, self._zero_coordinates))
            new_x = min(max(new_coordinates[0], 0), border_x - 1)
            if new_x in (0, border_x - 1):
                new_direction = random.choice(NEIGHBOURS_VALUES)
                while new_direction == self._direction:
                    new_direction = random.choice(NEIGHBOURS_VALUES)
                self._direction = new_direction

            new_y = min(max(new_coordinates[1], 0), border_y - 1)
            if new_y in (0, border_x - 1):
                new_direction = random.choice(NEIGHBOURS_VALUES)
                while new_direction == self._direction:
                    new_direction = random.choice(NEIGHBOURS_VALUES)
                self._direction = new_direction
            self._zero_coordinates = Cell(new_x, new_y)
