"""The module contains all world's processors
changing states of the world."""
import cv2
import logging
import random
import numpy as np

from resources.common_types import Colors
from src.world import World
from src.active_characters import Food, Worm


class WorldProcessor:
    """Base class of processors."""

    def __init__(self):
        pass

    def process(self, world_object: World) -> None:
        """Base method of processors."""


class Visualizer(WorldProcessor):
    """Visualizing processor."""

    def __init__(self, save_visualizations: bool = False):
        super(Visualizer, self).__init__()
        self.save_visualizations = save_visualizations
        self.count = 0

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

        if self.save_visualizations:
            cv2.imwrite(f'output/vis_{self.count}.png', vis)
            self.count += 1

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
            is_worm_in_danger = worm.is_dangerous(
                worm.max_danger_at_location(world_object.worms_at(worm.coordinates)))

            is_nothing_interesting_in_cell = False

            if len(affordable_food) == 0 and len(enemies) == 0:
                is_nothing_interesting_in_cell = True

            if is_worm_in_danger or is_nothing_interesting_in_cell:
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
