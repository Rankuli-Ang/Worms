"""The module contains World class
with all cell search methods."""
from typing import Dict, List
import random

from src.active_characters import Worm, Food, Genes, create_genome
from src.weather import Rain, Tornado
from resources.common_types import Neighbors, NEIGHBOURS_VALUES


class Cell:
    """Container with objects located at certain coordinates on the map."""

    def __init__(self):
        self.worms = []
        self.food = []


class World:
    """The main class in which the mechanics are implemented."""

    def __init__(self, height: int = 100, width: int = 100,
                 worms_num: int = 250, food_num: int = 1000):
        self.cells: Dict[tuple, Cell] = {}
        self.worms: List[Worm] = []
        self.food: List[Food] = []

        for y in range(height):
            for x in range(width):
                self.cells[(x, y)] = Cell()

        self.rains: List[Rain] = []
        self.tornadoes: List[Tornado] = []
        self.name: str = 'World'
        self.height = height
        self.width = width

        self.populate(worms_num)
        self.sow_food(food_num)

    def get_random_pos(self) -> tuple:
        """get a random coordinates on the map."""
        return random.randrange(0, self.width), random.randrange(0, self.height)

    def populate(self, worms_num: int = 250) -> None:
        """Places a given number of worms at random map coordinates."""
        for i in range(worms_num):
            pos = self.get_random_pos()
            worm = Worm(pos)
            worm.genetics.genotype = create_genome()
            worm.newborn_genetics_boost(worm.genetics.genotype)
            self.cells[pos].worms.append(worm)
            self.worms.append(worm)

    def sow_food(self, food_num: int = 1000) -> None:
        """Places a given number of food objects at random map coordinates."""
        for i in range(food_num):
            pos = self.get_random_pos()
            food_unit = Food(pos)
            self.cells[pos].food.append(food_unit)
            self.food.append(food_unit)

    def rain_emergence(self) -> None:
        """creates a new Rain object."""
        self.rains.append(Rain(self.get_random_pos()))

    def tornado_emergence(self) -> None:
        """creates a new Tornado object."""
        self.tornadoes.append(Tornado(self.get_random_pos()))

    @property
    def worms_by_initiative(self) -> List[Worm]:
        """Sorts list of worms by initiative."""
        return sorted(self.worms, key=lambda worm: worm.get_initiative())

    def worms_at(self, location_cell: tuple) -> List[Worm]:
        """Returns list of worms located on the cell."""
        if location_cell in self.cells:
            return self.cells[location_cell].worms
        return []

    def food_at(self, location_cell: tuple) -> List[Food]:
        """Returns list of food objects located on the cell."""
        if location_cell in self.cells:
            return self.cells[location_cell].food
        return []

    def has_food_at(self, location_cell: tuple) -> bool:
        """True if in the cell located food."""
        return location_cell in self.cells and len(self.cells[location_cell].food) > 0

    @staticmethod
    def move(pos, direction):
        """Changes coordinates."""
        return pos[0] + direction[0], pos[1] + direction[1]

    def get_neighbours_worms(self, location_cell: tuple, border_x: int, border_y: int) -> dict:
        """Returns dict(key=neighbours cell, value=list of worms in the cell)."""
        neighbours_worms = {}

        x, y = location_cell[0], location_cell[1]

        if y > 0:
            neighbours_worms[Neighbors.UP] = \
                self.worms_at(self.move(location_cell, Neighbors.UP.value))
        if y < border_y - 1:
            neighbours_worms[Neighbors.DOWN] = \
                self.worms_at(self.move(location_cell, Neighbors.DOWN.value))
        if x > 0:
            neighbours_worms[Neighbors.LEFT] = \
                self.worms_at(self.move(location_cell, Neighbors.LEFT.value))
        if x < border_x - 1:
            neighbours_worms[Neighbors.RIGHT] = \
                self.worms_at(self.move(location_cell, Neighbors.RIGHT.value))
        return neighbours_worms

    def get_neighbours_food(self, location_cell: tuple) -> List[Neighbors]:
        """Returns list of neighbours cells with food."""
        neighbours_food = []
        for val in NEIGHBOURS_VALUES:
            if self.has_food_at(self.move(location_cell, val)):
                neighbours_food.append(val)
        return neighbours_food

    def get_the_longest_genotype_at(self, location_cell: tuple) -> int:
        """Compares the genotype lengths of the worms in the cell
        and returns the highest value."""
        genotype_owners = self.worms_at(location_cell)
        lengths = [len(creature.genetics.genotype) for creature in genotype_owners]
        return max(lengths, default=0)

    def worms_is_not_relatives(self, location_cell: tuple) -> List[Worm]:
        """Returns a list of non-related worms with unique genotypes."""
        worms_at_location = self.worms_at(location_cell)
        if len(worms_at_location) == 1:
            return worms_at_location
        families: List[float] = []
        worms_is_not_relatives = []
        for worm in worms_at_location:
            if len(families) == 0:
                families.append(worm.genetics.family_affinity)
                worms_is_not_relatives.append(worm)
                continue
            overlap = False
            for family in families:
                if abs(worm.genetics.family_affinity - family) < 1e-12:
                    overlap = True
                    break
            if overlap is False:
                families.append(worm.genetics.family_affinity)
                worms_is_not_relatives.append(worm)
        return worms_is_not_relatives

    def genetic_variability(self, location_cell: tuple) -> List[Genes]:
        """Shuffles parental genotypes into a new one."""
        parents = self.worms_is_not_relatives(location_cell)
        if len(parents) == 1 and len(parents[0].genetics.genotype) > 0:
            return parents[0].genetics.genotype
        new_genotype = []
        new_genotype_length = self.get_the_longest_genotype_at(location_cell)
        gene_counter = 0
        while gene_counter <= new_genotype_length:
            if len(parents) > 0:
                for parent in parents:
                    try:
                        new_genotype.append(parent.genetics.genotype[gene_counter])

                    except IndexError:
                        parents.remove(parent)
                        gene_counter -= 1
                    gene_counter += 1
            else:
                break
        return new_genotype
