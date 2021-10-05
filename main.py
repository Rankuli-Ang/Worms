"""The module in which the visualization takes place,
the implementation of the mechanics
of worms, food, weather events."""
import configparser
import logging
import random
from typing import List, Dict
import cv2
import numpy as np

from common_types import Colors, Neighbors, NEIGHBOURS_VALUES
from weather import Rain, Tornado
from worm import Worm, Food, create_genome


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
        return sorted(world.worms, key=lambda worm: worm.get_initiative())

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
                world.worms_at(self.move(location_cell, Neighbors.UP.value))
        if y < border_y - 1:
            neighbours_worms[Neighbors.DOWN] = \
                world.worms_at(self.move(location_cell, Neighbors.DOWN.value))
        if x > 0:
            neighbours_worms[Neighbors.LEFT] = \
                world.worms_at(self.move(location_cell, Neighbors.LEFT.value))
        if x < border_x - 1:
            neighbours_worms[Neighbors.RIGHT] = \
                world.worms_at(self.move(location_cell, Neighbors.RIGHT.value))
        return neighbours_worms

    def get_neighbours_food(self, location_cell: tuple) -> list:
        """Returns list of neighbours cells with food."""
        neighbours_food = []
        for val in NEIGHBOURS_VALUES:
            if world.has_food_at(self.move(location_cell, val)):
                neighbours_food.append(val)
        return neighbours_food

    def get_the_longest_genotype_at(self, location_cell: tuple) -> int:
        """Compares the genotype lengths of the worms in the cell
        and returns the highest value."""
        genotype_owners = self.worms_at(location_cell)
        lengths = [len(creature.genetics.genotype) for creature in genotype_owners]
        return max(lengths, default=0)

    def worms_is_not_relatives(self, location_cell: tuple) -> list:
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

    def genetic_variability(self, location_cell: tuple) -> list:
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


class WorldProcessor:
    """Base class of processors."""

    def __init__(self):
        pass

    def process(self, world_object: World) -> None:
        """Base method of processors."""


class Visualizer(WorldProcessor):
    """Visualizing processor."""

    def process(self, world_object: World) -> None:
        """Visualize the map of world with objects
        from Worm and Weather modules."""
        vis = np.zeros((world_object.height, world_object.width, 3), dtype='uint8')
        worm_color = [Colors.WHITE, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        for rain in world_object.rains:
            for coordinate in rain.all_coordinates:
                vis[coordinate[1],
                    coordinate[0]] \
                    = Colors.SKY_BLUE.value
        for tornado in world_object.tornadoes:
            for coordinate in tornado.all_coordinates:
                vis[coordinate[1],
                    coordinate[0]] \
                    = Colors.GREY.value
        for worm in world_object.worms:
            if worm.get_generation() < 4:
                vis[worm.coordinates[1],
                    worm.coordinates[0]] \
                    = worm_color[int(worm.get_generation())].value
            else:
                vis[worm.coordinates[1],
                    worm.coordinates[0]] = Colors.WHITE.value

        for food_unit in world_object.food:
            vis[food_unit.coordinates[1],
                food_unit.coordinates[0]] \
                = Colors.FOOD.value

        scale = 4
        vis = cv2.resize(vis, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('vis', vis)
        cv2.waitKey(1)


class AddFoodProcessor(WorldProcessor):
    """Add food objects on the map every iteration."""

    def process(self, world_object: World) -> None:
        """Add food objects at the random coordinates on the map."""
        growth = random.randint(10, 20)
        for i in range(growth):
            pos = world_object.get_random_pos()
            food_unit = Food(pos)
            world_object.cells[pos].food.append(food_unit)
            world_object.food.append(food_unit)


class AgingProcessor(WorldProcessor):
    """Increase age of worms every iteration."""

    def process(self, world_object: World) -> None:
        """Increase age of worms."""
        for worm in world_object.worms:
            worm.age += 1


class ZeroEnergyProcessor(WorldProcessor):
    """Processor decreases health of worms without energy."""

    def process(self, world_object: World) -> None:
        """Slowly decrease health of worms without energy."""
        for worm in world_object.worms_by_initiative:
            if worm.get_energy() <= 0:
                worm.health -= 0.1


class WormsMovementProcessor(WorldProcessor):
    """Processor moves worms on the map."""

    def process(self, world_object: World) -> None:
        """The worms assess the danger and the presence of food
         in neighboring cells, then move to a random one of the most acceptable. """
        for worm in world_object.worms_by_initiative:
            if worm.dead:
                continue
            enemies = [enemy for enemy in world_object.worms_at(worm.coordinates)
                       if enemy is not worm]
            affordable_food = world_object.food_at(worm.coordinates)
            if worm.is_dangerous(
                    worm.max_danger_at_location(world_object.worms_at(worm.coordinates))
            ) or (len(affordable_food) == 0 and len(enemies) == 0):
                neighbours_worms = world_object.get_neighbours_worms(
                    worm.coordinates, world_object.width, world_object.height)
                safe_steps = worm.get_safe_steps(neighbours_worms)
                if len(safe_steps) != 0:
                    steps_with_food = world_object.get_neighbours_food(worm.coordinates)
                    dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))

                    world_object.cells[worm.coordinates].worms.remove(worm)
                    worm.move(dcoord, world_object.width, world_object.height)
                    world_object.cells[worm.coordinates].worms.append(worm)


class PoisonProcessor(WorldProcessor):
    """Processor of poison effects on the worms."""

    def process(self, world_object: World) -> None:
        """If the worm is poisoned, it loses its life."""
        for worm in world_object.worms_by_initiative:
            worm.poison_effect()


class FightProcessor(WorldProcessor):
    """Processor of worms strikes."""

    def process(self, world_object: World) -> None:
        """Every worm strikes another not a relatives worm
        at the same cell."""
        for worm in world_object.worms_by_initiative:
            targets = world_object.worms_at(worm.coordinates)
            if len(targets) == 0:
                continue
            target = random.choice(targets)

            if target is worm:
                continue

            if worm.is_relative_to(target):
                continue

            worm.strike(target)
            target.strike(worm)


class LevelUpProcessor(WorldProcessor):
    """Processor of level ups effects."""

    def process(self, world_object: World) -> None:
        """Each worm that has reached
        a certain value of experience increases its level."""
        for worm in world_object.worms:
            worm.level_up()


class FoodPickUpProcessor(WorldProcessor):
    """Processor of pick ups food objects by worms."""

    def process(self, world_object: World) -> None:
        """Each worm picks up food if it is in the cage."""
        for eater in world_object.worms_by_initiative:
            targets = world_object.food_at(eater.coordinates)
            if len(targets) != 0:
                target = random.choice(targets)
                eater.eat(target)


class EatenFoodRemover(WorldProcessor):
    """Processor delete eaten food."""

    def process(self, world_object: World) -> None:
        """delete all food without nutritional value."""
        eaten_food = [food_unit for food_unit in world_object.food if food_unit.eaten]
        for food in eaten_food:
            world_object.cells[food.coordinates].food.remove(food)
            world_object.food.remove(food)


class CorpseGrindingProcessor(WorldProcessor):
    """Processor goes through the list of worms,
    if there are dead in their cells,
    the living receive a bonus."""

    def process(self, world_object: World) -> None:
        """Worms receive a bonus for killed worms in the same cell as they are."""
        for worm in world_object.worms:
            if not worm.dead:
                continue

            eaters = world_object.worms_at(worm.coordinates)
            for eater in eaters:
                if eater.dead:
                    continue
                eater.health += worm.get_level() + worm.get_damage() + worm.get_initiative()
                eater.energy += (worm.get_level() + worm.get_damage() + worm.get_initiative()) * 10


class DeadWormsRemover(WorldProcessor):
    """Processor goes through the list of worms if they are dead and removes them."""

    def __init__(self):
        super().__init__()
        self.dead_worms = 0

    def process(self, world_object: World) -> None:
        """Delete dead worms."""
        number_of_worms_before = len(world_object.worms)
        dead_worms = [worm for worm in world_object.worms if worm.dead]
        for worm in dead_worms:
            cell = world_object.cells[worm.coordinates]
            cell.worms.remove(worm)
            world_object.worms.remove(worm)
        dead_worms_in_round = number_of_worms_before - len(world_object.worms)
        self.dead_worms += dead_worms_in_round
        print('dead', self.dead_worms)


class WormDivisionProcessor(WorldProcessor):
    """Creates new worms with genotypes derived from parental worms."""

    def process(self, world_object: World) -> None:
        """Creates a worm with a parental genotype
        or with a genotype mixed from the genotypes
        of non-relatives worms in the cell."""
        for parent in world_object.worms:
            if parent.get_divisions_limit() == 0:
                continue
            child = Worm(parent.coordinates)
            child.genetics.genotype = world_object.genetic_variability(parent.coordinates)
            world_object.cells[parent.coordinates].worms.append(child)
            world_object.worms.append(child)
            child.genetics.family_affinity = parent.genetics.family_affinity + 0.00000000000001
            child.newborn_genetics_boost(child.genetics.genotype)
            parent.divisions_limit -= 1
            child.generation = parent.get_generation() + 1


class MutationProcessor(WorldProcessor):
    """Creates a random changes in the worm's genotype."""

    def process(self, world_object: World) -> None:
        """With a certain probability creates
        a random change in the worm's genotype
        (add, del or exchange gene)."""
        for worm in world_object.worms:
            mutation_probability_throw = random.randint(1, 100)
            worm.mutation_metamorphosis(mutation_probability_throw)


class WeatherEventsEmergenceProcessor(WorldProcessor):
    """Creates a new weather objects."""

    def process(self, world_object: World) -> None:
        """With a certain probability creates
        a new Rain or Tornado object."""
        if len(world_object.rains) < 5:
            chance_throw = random.randrange(0, 10)
            if chance_throw >= 8:
                world_object.rain_emergence()

        if len(world_object.tornadoes) < 3:
            chance_throw = random.randrange(0, 10)
            if chance_throw >= 8:
                world_object.tornado_emergence()


class WeatherMovementsProcessor(WorldProcessor):
    """Moves weather objects on the map."""

    def process(self, world_object: World) -> None:
        """Moves weather objects and update list of occupied coordinates."""
        if world_object.rains:
            for rain in world_object.rains:
                rain.move(world_object.width, world_object.height)
                rain.upscaling(world_object.width, world_object.height)

        if world_object.tornadoes:
            for tornado in world_object.tornadoes:
                tornado.move(world_object.width, world_object.height)
                tornado.upscaling(world_object.width, world_object.height)


class WeatherEffectsProcessor(WorldProcessor):
    """Applies effects of the weather objects."""

    def process(self, world_object: World) -> None:
        """Tornado scatters worms and food,
        Rain decrease health/energy of worms
        and decrease nutritional_value of food."""
        if len(world_object.rains) > 0:
            for rain in world_object.rains:
                for coordinate in rain.all_coordinates:
                    worms_in_cell = world_object.worms_at(coordinate)
                    food_in_cell = world_object.food_at(coordinate)
                    rain.raining_effect(worms_in_cell, food_in_cell)

        if len(world_object.tornadoes) > 0:
            for tornado in world_object.tornadoes:
                for coordinate in tornado.all_coordinates:
                    worms_in_cell = world_object.worms_at(coordinate)
                    food_in_cell = world_object.food_at(coordinate)
                    cell = world_object.cells[coordinate]
                    cell.worms = []
                    cell.food = []
                    tornado.tornado_effect(worms_in_cell, food_in_cell,
                                           world_object.width, world_object.height)
                    for worm in worms_in_cell:
                        world_object.cells[worm.coordinates].worms.append(worm)
                    for food in food_in_cell:
                        world_object.cells[food.coordinates].food.append(food)


class WeatherEventsRemover(WorldProcessor):
    """Delete expired weather objects."""

    def process(self, world_object: World) -> None:
        """If duration of weather objects is over
        delete the weather object."""
        for rain in world_object.rains:
            if rain.duration <= 0:
                world_object.rains.remove(rain)

        for tornado in world_object.tornadoes:
            if tornado.duration <= 0:
                world_object.tornadoes.remove(tornado)


class AnalyticsProcessor(WorldProcessor):
    """Displays info in the console."""

    def __init__(self):
        super().__init__()
        self.iterations = 0
        self.step = 0

    def process(self, world_object: World) -> None:
        """Displays iteration number and total number of worms on the map."""
        self.iterations += 1
        self.step += 1
        print('iter', self.iterations)
        print('number of worms', len(world_object.worms))
        if self.step == 100:
            logging.debug('Program is working correctly')
            self.step = 0


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')
    logging_levels = {'DEBUG': logging.DEBUG,
                      'INFO': logging.INFO,
                      'WARNING': logging.WARNING,
                      'ERROR': logging.ERROR,
                      'CRITICAL': logging.CRITICAL}

    logging_level = config.get('LOGGER', 'level')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging_levels.get(logging_level))

    WORLD_HEIGHT = int(config.get('WORLD', 'height'))
    WORLD_WIDTH = int(config.get('WORLD', 'width'))
    WORLD_START_WORMS_NUM = int(config.get('WORLD', 'worms_num'))
    WORLD_START_FOOD_NUM = int(config.get('WORLD', 'food_num'))

    world = World(WORLD_HEIGHT, WORLD_WIDTH, WORLD_START_WORMS_NUM, WORLD_START_FOOD_NUM)
    valid_processors = {
        'agingprocessor': AgingProcessor,
        'zeroenergyprocessor': ZeroEnergyProcessor,
        'poisonprocessor': PoisonProcessor,
        'weathereventsemergenceprocessor': WeatherEventsEmergenceProcessor,
        'addfoodprocessor': AddFoodProcessor,
        'weathermovementsprocessor': WeatherMovementsProcessor,
        'weathereffectsprocessor': WeatherEffectsProcessor,
        'wormsmovementprocessor': WormsMovementProcessor,
        'fightprocessor': FightProcessor,
        'corpsegrindingprocessor': CorpseGrindingProcessor,
        'foodpickupprocessor': FoodPickUpProcessor,
        'deadwormsremover': DeadWormsRemover,
        'eatenfoodremover': EatenFoodRemover,
        'weathereventsremover': WeatherEventsRemover,
        'levelupprocessor': LevelUpProcessor,
        'wormdivisionprocessor': WormDivisionProcessor,
        'mutationprocessor': MutationProcessor,
        'analyticsprocessor': AnalyticsProcessor,
        'visualizer': Visualizer}

    processors = []

    for option in config.options('PROCESSORS'):
        if option not in valid_processors.keys():
            logging.error('Unknown processor')
            raise ValueError('Unknown processor')
        if config.getboolean('PROCESSORS', option) is True:
            proc = valid_processors[option]
            processors.append(proc())

    PROCESS = True

    while PROCESS is True:
        for proc in processors:
            proc.process(world)
