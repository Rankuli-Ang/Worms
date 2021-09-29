import configparser
from os import path
import logging
import logging.config
import random
from typing import List, Dict
from cv2 import cv2
import numpy as np

from common_types import Colors, Cell, Neighbors, NEIGHBOURS_VALUES
from weather import Rain, Tornado
from worm import Worm, Food, create_genome


# rename to just Cell
class WorldCell:
    """Container with objects located at certain coordinates on the map."""

    def __init__(self):
        self.worms = []
        self.food = []


class World:
    def __init__(self, height: int = 100, width: int = 100,
                 worms_num: int = 250, food_num: int = 1000):
        self.cells: Dict[Cell, WorldCell] = {}
        self.worms: List[Worm] = []
        self.food: List[Food] = []

        for y in range(height):
            for x in range(width):
                self.cells[Cell(x, y)] = WorldCell()

        self.rains: List[Rain] = []
        self.tornadoes: List[Tornado] = []
        self.name: str = 'World'
        self.height = height
        self.width = width

        self.populate(worms_num)
        self.sow_food(food_num)

    def get_random_pos(self) -> Cell:
        return Cell(random.randrange(0, self.width), random.randrange(0, self.height))

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
        self.rains.append(Rain(self.get_random_pos()))

    def tornado_emergence(self) -> None:
        self.tornadoes.append(Tornado(self.get_random_pos()))

    @property
    def worms_by_initiative(self) -> List[Worm]:
        return sorted(world.worms, key=lambda worm: worm.get_initiative())

    def worms_at(self, location_cell: tuple) -> List[Worm]:
        # if location_cell in self.cells:
        return self.cells[location_cell].worms
        # return []

    def food_at(self, location_cell: tuple) -> List[Food]:
        # if location_cell in self.cells:
        return self.cells[location_cell].food
        # return []

    def has_food_at(self, location_cell: Cell) -> bool:
        return location_cell in self.cells and len(self.cells[location_cell].food) > 0

    @staticmethod
    def move(pos, direction):
        return Cell(pos[0] + direction[0], pos[1] + direction[1])

    def get_neighbours_worms(self, location_cell: tuple, border_x: int, border_y: int) -> dict:
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
        neighbours_food = []
        for val in NEIGHBOURS_VALUES:
            if world.has_food_at(self.move(location_cell, val)):
                neighbours_food.append(val)
        return neighbours_food

    def get_the_longest_genotype_at(self, location_cell: tuple) -> int:
        genotype_owners = self.worms_at(location_cell)
        lengths = [len(creature.genetics.genotype) for creature in genotype_owners]
        return max(lengths, default=0)

    def worms_is_not_relatives(self, location_cell: tuple) -> list:
        worms_at_location = self.worms_at(location_cell)
        if len(worms_at_location) == 1:
            return worms_at_location
        families = []
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
    """Skeleton class for processors"""

    def __init__(self):
        pass

    def process(self, world_object: World) -> None:
        pass


class Visualizer(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        vis = np.zeros((world_object.height, world_object.width, 3), dtype='uint8')
        worm_color = [Colors.WHITE, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        for rain in world_object.rains:
            for coordinate in rain.all_coordinates:
                vis[coordinate.__getattribute__('y'),
                    coordinate.__getattribute__('x')] \
                    = Colors.SKY_BLUE.value
        for tornado in world_object.tornadoes:
            for coordinate in tornado.all_coordinates:
                vis[coordinate.__getattribute__('y'),
                    coordinate.__getattribute__('x')] \
                    = Colors.GREY.value
        for worm in world_object.worms:
            if worm.get_generation() < 4:
                vis[worm.coordinates.__getattribute__('y'),
                    worm.coordinates.__getattribute__('x')] \
                    = worm_color[worm.get_generation()].value
            else:
                vis[worm.coordinates.__getattribute__('y'),
                    worm.coordinates.__getattribute__('x')] = Colors.WHITE.value

        for food_unit in world_object.food:
            vis[food_unit.coordinates.__getattribute__('y'),
                food_unit.coordinates.__getattribute__('x')] \
                = Colors.FOOD.value

        scale = 4
        vis = cv2.resize(vis, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('vis', vis)
        cv2.waitKey(1)


class AddFoodProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        growth = random.randint(10, 20)
        for i in range(growth):
            pos = world_object.get_random_pos()
            food_unit = Food(pos)
            world_object.cells[pos].food.append(food_unit)
            world_object.food.append(food_unit)


class AgingProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms:
            worm.age += 1


class ZeroEnergyProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            if worm.get_energy() <= 0:
                worm.health -= 0.1


class WormsMovementProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            if worm.dead:
                continue
            enemies = [enemy for enemy in world_object.worms_at(worm.coordinates)
                       if enemy is not worm]
            targets = world_object.food_at(worm.coordinates)
            if len(enemies) == 0 and len(targets) > 0:
                continue
            elif not worm.is_dangerous \
                        (worm.max_danger_at_location(world_object.worms_at(worm.coordinates))) \
                    and len(targets) > 0:
                continue
            else:
                neighbours_worms = world_object.get_neighbours_worms \
                    (worm.coordinates, world_object.width, world_object.height)
                safe_steps = worm.get_safe_steps(neighbours_worms)
                if len(safe_steps) == 0:
                    continue
                else:
                    steps_with_food = world_object.get_neighbours_food(worm.coordinates)
                    dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))

                    world_object.cells[worm.coordinates].worms.remove(worm)
                    worm.move(dcoord, world_object.width, world_object.height)
                    world_object.cells[worm.coordinates].worms.append(worm)


class PoisonProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            worm.poison_effect()


class FightProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
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
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms:
            worm.level_up()


class FoodPickUpProcessor(WorldProcessor):
    def __init__(self):
        super(FoodPickUpProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for eater in world_object.worms_by_initiative:
            targets = world_object.food_at(eater.coordinates)
            if len(targets) != 0:
                target = random.choice(targets)
                eater.eat(target)


class EatenFoodRemover(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        eaten_food = [food_unit for food_unit in world_object.food if food_unit.eaten]
        for food in eaten_food:
            world_object.cells[food.coordinates].food.remove(food)
            world_object.food.remove(food)


class CorpseGrindingProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
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
    def __init__(self):
        super().__init__()
        self.dead_worms = 0

    def process(self, world_object: World) -> None:
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
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for parent in world_object.worms:
            if parent.get_divisions_limit() == 0:
                continue
            child = Worm(parent.coordinates)
            child.genetics.genotype = world_object.genetic_variability(parent.coordinates)
            world_object.cells[parent.coordinates].worms.append(child)
            world_object.worms.append(child)
            child.family_affinity = parent.genetics.family_affinity + 0.00000000000001
            child.newborn_genetics_boost(child.genetics.genotype)
            parent.divisions_limit -= 1
            child.generation = parent.get_generation() + 1


class MutationProcessor(WorldProcessor):
    def __int__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms:
            mutation_saving_throw = random.randint(1, 100)
            happened_mutation = []
            if mutation_saving_throw == 1:
                happened_mutation.append('substitution_mutation')
            elif 1 < mutation_saving_throw < 4:
                happened_mutation.append('insertion_mutation')
            elif 3 < mutation_saving_throw < 6:
                happened_mutation.append('deletion_mutation')

            if len(happened_mutation) == 0:
                continue
            else:
                worm.mutation_metamorphosis(happened_mutation[0])


class WeatherEventsEmergenceProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        if len(world_object.rains) < 5:
            chance_throw = random.randrange(0, 10)
            if chance_throw >= 8:
                world_object.rain_emergence()

        if len(world_object.tornadoes) < 3:
            chance_throw = random.randrange(0, 10)
            if chance_throw >= 8:
                world_object.tornado_emergence()


class WeatherMovementsProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        if len(world_object.rains) > 0:
            for rain in world_object.rains:
                rain.move(world_object.width, world_object.height)
                rain.upscaling(world_object.width, world_object.height)

        if len(world_object.tornadoes) > 0:
            for tornado in world_object.tornadoes:
                tornado.move(world_object.width, world_object.height)
                tornado.upscaling(world_object.width, world_object.height)


class WeatherEffectsProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
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
    def __init__(self):
        super().__init__()

    def process(self, world_object: World) -> None:
        for rain in world_object.rains:
            if rain.duration <= 0:
                world_object.rains.remove(rain)

        for tornado in world_object.tornadoes:
            if tornado.duration <= 0:
                world_object.tornadoes.remove(tornado)


class AnalyticsProcessor(WorldProcessor):
    def __init__(self):
        super().__init__()
        self.iterations = 0

    def process(self, world_object: World) -> None:
        self.iterations += 1
        print('iter', self.iterations)
        print('number of worms', len(world_object.worms))


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')

    log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf.ini')
    logging.config.fileConfig(log_file_path)

    logging.config.fileConfig(log_file_path)

    logging.basicConfig(filename='sum.log', level=logging.INFO)
    logger = logging.getLogger('test_logger')

    fh = logging.FileHandler('errors.log')
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.warning('warning')
    logger.info('check')
    logger.error('ERROR!!!')

    world_height = int(config.get('WORLD', 'height'))
    world_width = int(config.get('WORLD', 'width'))
    world_worms_num = int(config.get('WORLD', 'worms_num'))
    world_food_num = int(config.get('WORLD', 'food_num'))

    print(config.options('PROCESSORS'))

    world = World(world_height, world_width, world_worms_num, world_food_num)
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

    t = 0
    tt = True

    while tt is True:
        t += 1
        for proc in processors:
            proc.process(world)
        if t >= 100:
            tt = False
    logging.info('program is ended correctly')
