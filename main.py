import random
from typing import List
from operator import add
from common_types import Colors, Cell, Neighbors

import cv2
import numpy as np

from worm import Worm, Food, create_genome


class World:
    def __init__(self, height: int = 100, width: int = 100, worms_num: int = 250, food_num: int = 1000):
        self.worms: List[Worm] = []
        self.food: List[Food] = []
        self.name: str = 'World'
        self.height = height
        self.width = width

        World.populate_world(self, worms_num)
        World.sow_food(self, food_num)

    def populate_world(self, worms_num: int = 250) -> None:
        for i in range(worms_num):
            worm = Worm(Cell(random.randrange(0, self.width), random.randrange(0, self.height)))
            worm.genetics.genotype = create_genome()
            worm.newborn_genetics_boost(worm.genetics.genotype)
            self.worms.append(worm)

    def sow_food(self, food_num: int = 1000) -> None:
        for i in range(food_num):
            food_unit = Food(Cell(random.randrange(0, self.width), random.randrange(0, self.height)))
            self.food.append(food_unit)

    @property
    def worms_by_initiative(self) -> List[Worm]:
        return sorted(world.worms, key=lambda worm: worm.get_initiative())

    def worms_at(self, location_cell: tuple) -> List[Worm]:
        return [worm for worm in self.worms if
                worm.coordinates == location_cell]

    def food_at(self, location_cell: tuple) -> List[Food]:
        return [food_unit for food_unit in self.food
                if food_unit.coordinates == location_cell]

    def get_neighbours_worms(self, location_cell: tuple, border_x: int, border_y: int) -> dict:
        neighbours_worms = {}

        if location_cell.__getattribute__('y') > 0:
            up = {Neighbors.UP: world.worms_at(tuple(map(add, location_cell, Neighbors.UP.value)))}
            neighbours_worms.update(up)
        if location_cell.__getattribute__('y') < border_y:
            down = {Neighbors.DOWN: world.worms_at(tuple(map(add, location_cell, Neighbors.DOWN.value)))}
            neighbours_worms.update(down)
        if location_cell.__getattribute__('x') > 0:
            left = {Neighbors.LEFT: world.worms_at(tuple(map(add, location_cell, Neighbors.LEFT.value)))}
            neighbours_worms.update(left)
        if location_cell.__getattribute__('x') < border_x:
            right = {Neighbors.RIGHT: world.worms_at(tuple(map(add, location_cell, Neighbors.RIGHT.value)))}
            neighbours_worms.update(right)
        return neighbours_worms

    def get_neighbours_food(self, location_cell: tuple, border_x: int, border_y: int) -> list:
        neighbours_food = []

        if location_cell.__getattribute__('y') > 0:
            up = {Neighbors.UP: world.food_at(tuple(map(add, location_cell, Neighbors.UP.value)))}
            if len(up.get(Neighbors.UP)) > 0:
                neighbours_food.append(Neighbors.UP.value)
        if location_cell.__getattribute__('y') < border_y:
            down = {Neighbors.DOWN: world.food_at(tuple(map(add, location_cell, Neighbors.DOWN.value)))}
            if len(down.get(Neighbors.DOWN)) > 0:
                neighbours_food.append(Neighbors.DOWN.value)
        if location_cell.__getattribute__('x') > 0:
            left = {Neighbors.LEFT: world.food_at(tuple(map(add, location_cell, Neighbors.LEFT.value)))}
            if len(left.get(Neighbors.LEFT)) > 0:
                neighbours_food.append(Neighbors.LEFT.value)
        if location_cell.__getattribute__('x') < border_x:
            right = {Neighbors.RIGHT: world.food_at(tuple(map(add, location_cell, Neighbors.RIGHT.value)))}
            if len(right.get(Neighbors.RIGHT)) > 0:
                neighbours_food.append(Neighbors.RIGHT.value)
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
        parents = self.worms_is_not_relatives(location_cell)
        if len(parents) == 1:
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
    def __init__(self):
        pass

    def process(self, world_object: World) -> None:
        pass


class Visualizer(WorldProcessor):
    def __init__(self):
        super(Visualizer, self).__init__()

    def process(self, world_object: World) -> None:
        vis = np.zeros((world_object.height, world_object.width, 3), dtype='uint8')
        worm_color = [Colors.WHITE, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        for worm in world_object.worms:
            if worm.get_generation() < 4:
                vis[worm.coordinates.__getattribute__('y'), worm.coordinates.__getattribute__('x')] \
                    = worm_color[worm.get_generation()].value
            else:
                vis[worm.coordinates.__getattribute__('y'), worm.coordinates.__getattribute__('x')] = Colors.WHITE.value

        for food_unit in world_object.food:
            vis[food_unit.coordinates.__getattribute__('y'), food_unit.coordinates.__getattribute__('x')] \
                = Colors.FOOD.value

        scale = 4
        vis = cv2.resize(vis, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('vis', vis)
        cv2.waitKey(1)


class AddFoodProcessor(WorldProcessor):
    def __init__(self):
        super(AddFoodProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        growth = random.randint(10, 20)
        for i in range(growth):
            food_unit = Food(Cell(random.randrange(0, world_object.width), random.randrange(0, world_object.height)))
            world_object.food.append(food_unit)


class AgingProcessor(WorldProcessor):
    def __init__(self):
        super(AgingProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms:
            worm.age += 1


class ZeroEnergyProcessor(WorldProcessor):
    def __init__(self):
        super(ZeroEnergyProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            if worm.get_energy() <= 0:
                worm.health -= 0.1


class MovementProcessor(WorldProcessor):
    def __init__(self):
        super(MovementProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            if worm.dead:
                continue
            enemies = [enemy for enemy in world_object.worms_at(worm.coordinates) if enemy is not worm]
            targets = world_object.food_at(worm.coordinates)
            if len(enemies) == 0 and len(targets) > 0:
                continue
            elif not worm.is_dangerous(worm.max_danger_at_location(world_object.worms_at(worm.coordinates))) \
                    and len(targets) > 0:
                continue
            else:
                neighbours_worms = world_object.get_neighbours_worms(worm.coordinates, world_object.width,
                                                                     world_object.height)
                safe_steps = worm.get_safe_steps(neighbours_worms)
                if len(safe_steps) == 0:
                    continue
                else:
                    steps_with_food = world_object.get_neighbours_food(worm.coordinates, world_object.width,
                                                                       world_object.height)
                    dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))
                    worm.move(dcoord, world_object.width, world_object.height)


class PoisonProcessor(WorldProcessor):
    def __init__(self):
        super(PoisonProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            if worm.get_poisoned() > 0:
                worm.health -= 1
                worm.poisoned -= 1


class FightProcessor(WorldProcessor):
    def __init__(self):
        super(FightProcessor, self).__init__()

    def process(self, world_object: World) -> None:
        for worm in world_object.worms_by_initiative:
            targets = world_object.worms_at(worm.coordinates)
            target = random.choice(targets)

            if target is worm:
                continue

            if worm.is_relative_to(target):
                continue

            worm.strike(target)
            target.strike(worm)


class LevelUpProcessor(WorldProcessor):
    def __init__(self):
        super(LevelUpProcessor, self).__init__()

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
        super(EatenFoodRemover, self).__init__()

    def process(self, world_object: World) -> None:
        world_object.food = [food_unit for food_unit in world_object.food if not food_unit.eaten]


class CorpseGrindingProcessor(WorldProcessor):
    def __init__(self):
        super(CorpseGrindingProcessor, self).__init__()

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
        super(DeadWormsRemover, self).__init__()
        self.dead_worms = 0

    def process(self, world_object: World) -> None:
        number_of_worms_before = len(world_object.worms)
        alive_worms = [worm for worm in world_object.worms if not worm.dead]
        world_object.worms = alive_worms
        dead_worms_in_round = number_of_worms_before - len(world_object.worms)
        self.dead_worms += dead_worms_in_round
        print('dead', self.dead_worms)


class WormDivision(WorldProcessor):
    def __init__(self):
        super(WormDivision, self).__init__()

    def process(self, world_object: World) -> None:
        for parent in world_object.worms:
            if parent.get_divisions_limit() == 0:
                continue
            child = Worm(parent.coordinates)
            child.genetics.genotype = world_object.genetic_variability(parent.coordinates)
            child.family_affinity = parent.genetics.family_affinity + 0.00000000000001
            child.newborn_genetics_boost(child.genetics.genotype)
            world_object.worms.append(child)
            parent.divisions_limit -= 1
            child._generation = parent.get_generation() + 1


class MutationProcessor(WorldProcessor):
    def __int__(self):
        super(MutationProcessor, self).__init__()

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


class AnalyticsProcessor(WorldProcessor):
    def __init__(self):
        super(AnalyticsProcessor, self).__init__()
        self.iterations = 0

    def process(self, world_object: World) -> None:
        self.iterations += 1
        print('iter', self.iterations)
        print('number of worms', len(world_object.worms))


if __name__ == "__main__":
    world = World(100, 100, 250, 1000)

    processors = [AgingProcessor(), ZeroEnergyProcessor(), PoisonProcessor(), MovementProcessor(), FightProcessor(),
                  CorpseGrindingProcessor(), DeadWormsRemover(),
                  FoodPickUpProcessor(), EatenFoodRemover(), AddFoodProcessor(),
                  LevelUpProcessor(), WormDivision(), MutationProcessor(),
                  AnalyticsProcessor(), Visualizer()]

    while True:
        for proc in processors:
            proc.process(world)
