import random
from typing import List
from enum import Enum

import cv2
import numpy as np

from worm import Worm, Food, create_genome, cell, Neighbors


class Colors(Enum):
    SPACE = (0, 0, 0)
    FOOD = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (0, 255, 255)


class World:
    def __init__(self, height: int = 100, width: int = 100, worms_num: int = 250, food_num: int = 1000):
        self.worms: List[Worm] = []
        self.food: List[Food] = []
        self.name: str = 'World'
        self.height = height
        self.width = width

        World.populate_world(self, worms_num)
        World.sow_food(self, food_num)

    def populate_world(self, worms_num: int = 250):
        for i in range(worms_num):
            genotype = create_genome()
            worm = Worm(random.randrange(0, self.width), random.randrange(0, self.height))
            worm.genotype = genotype
            for gene in worm.genotype:
                worm.genetical_boost(gene)
            self.worms.append(worm)

    def sow_food(self, food_num: int = 1000):
        for i in range(food_num):
            food_unit = Food(random.randrange(0, self.width), random.randrange(0, self.height))
            self.food.append(food_unit)

    @property
    def worms_by_initiative(self) -> List[Worm]:
        return sorted(world.worms, key=lambda worm: worm.initiative)

    def worms_at(self, location_cell: cell) -> List[Worm]:
        return [worm for worm in self.worms if
                worm.coordinates.__getattribute__('x') == location_cell.__getattribute__('x')
                and worm.coordinates.__getattribute__('y') == location_cell.__getattribute__('y')]

    def food_at(self, location_cell: cell) -> List[Food]:
        return [food_unit for food_unit in self.food
                if food_unit.coordinates.__getattribute__('x') == location_cell.__getattribute__('x')
                and food_unit.coordinates.__getattribute__('y') == location_cell.__getattribute__('y')]

    def get_neighbours_worms(self, location_cell: cell, border_x: int, border_y: int) -> dict:
        neighbours_worms = {}

        if location_cell.__getattribute__('y') > 0:
            up = {Neighbors.UP: world.worms_at(cell(location_cell.__getattribute__('x'),
                                                    (location_cell.__getattribute__('y') - 1)))}
            neighbours_worms.update(up)
        if location_cell.__getattribute__('y') < border_y:
            down = {Neighbors.DOWN: world.worms_at(cell(location_cell.__getattribute__('x'),
                                                        (location_cell.__getattribute__('y') + 1)))}
            neighbours_worms.update(down)
        if location_cell.__getattribute__('x') > 0:
            left = {Neighbors.LEFT: world.worms_at(cell((location_cell.__getattribute__('x') - 1),
                                                        location_cell.__getattribute__('y')))}
            neighbours_worms.update(left)
        if location_cell.__getattribute__('x') < border_x:
            right = {Neighbors.RIGHT: world.worms_at(cell((location_cell.__getattribute__('x') + 1),
                                                          location_cell.__getattribute__('y')))}
            neighbours_worms.update(right)
        return neighbours_worms

    def get_neighbours_food(self, location_cell: cell, border_x: int, border_y: int) -> list:
        neighbours_food = []

        if location_cell.__getattribute__('y') > 0:
            up = {Neighbors.UP: world.food_at(cell(location_cell.__getattribute__('x'),
                                                   (location_cell.__getattribute__('y') - 1)))}
            if len(up.get(Neighbors.UP)) > 0:
                neighbours_food.append(Neighbors.UP.value)
        if location_cell.__getattribute__('y') < border_y:
            down = {Neighbors.DOWN: world.food_at(cell(location_cell.__getattribute__('x'),
                                                       (location_cell.__getattribute__('y') + 1)))}
            if len(down.get(Neighbors.DOWN)) > 0:
                neighbours_food.append(Neighbors.DOWN.value)
        if location_cell.__getattribute__('x') > 0:
            left = {Neighbors.LEFT: world.food_at(cell((location_cell.__getattribute__('x') - 1),
                                                       location_cell.__getattribute__('y')))}
            if len(left.get(Neighbors.LEFT)) > 0:
                neighbours_food.append(Neighbors.LEFT.value)
        if location_cell.__getattribute__('x') < border_x:
            right = {Neighbors.RIGHT: world.food_at(cell((location_cell.__getattribute__('x') + 1),
                                                         location_cell.__getattribute__('y')))}
            if len(right.get(Neighbors.RIGHT)) > 0:
                neighbours_food.append(Neighbors.RIGHT.value)
        return neighbours_food


class WorldProcessor:
    def __init__(self):
        pass

    def process(self, world: World) -> None:
        pass


class Visualizer(WorldProcessor):
    def __init__(self):
        super(Visualizer, self).__init__()

    def process(self, world: World) -> None:
        vis = np.zeros((world.height, world.width, 3), dtype='uint8')
        worm_color = [Colors.WHITE, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        for worm in world.worms:
            if worm.generation < 4:
                vis[worm.coordinates.__getattribute__('y'), worm.coordinates.__getattribute__('x')] \
                    = worm_color[worm.generation].value
            else:
                vis[worm.coordinates.__getattribute__('y'), worm.coordinates.__getattribute__('x')] = Colors.WHITE.value

        for food_unit in world.food:
            vis[food_unit.y, food_unit.x] = Colors.FOOD.value

        scale = 4
        vis = cv2.resize(vis, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('vis', vis)
        cv2.waitKey(1)


class AddFoodProcessor(WorldProcessor):
    def __init__(self):
        super(AddFoodProcessor, self).__init__()

    def process(self, world: World) -> None:
        growth = random.randint(10, 20)
        for i in range(growth):
            food_unit = Food(random.randrange(0, world.width), random.randrange(0, world.height))
            world.food.append(food_unit)


class AgingProcessor(WorldProcessor):
    def __init__(self):
        super(AgingProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms:
            worm.age += 1


class ZeroEnergyProcessor(WorldProcessor):
    def __init__(self):
        super(ZeroEnergyProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            if worm.energy <= 0:
                worm.health -= 0.1


class MovementProcessor(WorldProcessor):
    def __init__(self):
        super(MovementProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            if worm.dead:
                continue
            enemies = [enemy for enemy in world.worms_at(worm.coordinates) if enemy is not worm]
            targets = world.food_at(worm.coordinates)
            if len(enemies) == 0 and len(targets) > 0:
                continue
            elif not worm.is_dangerous(worm.max_danger_at_location(world.worms_at(worm.coordinates)))\
                    and len(targets) > 0:
                continue
            else:
                neighbours_worms = world.get_neighbours_worms(worm.coordinates, world.width, world.height)
                safe_steps = worm.get_safe_steps(neighbours_worms)
                if len(safe_steps) == 0:
                    continue
                else:
                    steps_with_food = world.get_neighbours_food(worm.coordinates, world.width, world.height)
                    dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))
                    worm.move(dcoord, world.width, world.height)


class PoisonProcessor(WorldProcessor):
    def __init__(self):
        super(PoisonProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            if worm.poisoned > 0:
                worm.health -= 1
                worm.poisoned -= 1


class FightProcessor(WorldProcessor):
    def __init__(self):
        super(FightProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            targets = world.worms_at(worm.coordinates)
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

    def process(self, world: World) -> None:
        for worm in world.worms:
            worm.level_up()


class FoodPickUpProcessor(WorldProcessor):
    def __init__(self):
        super(FoodPickUpProcessor, self).__init__()

    def process(self, world: World) -> None:
        for eater in world.worms_by_initiative:
            targets = world.food_at(eater.coordinates)
            if len(targets) != 0:
                target = random.choice(targets)
                eater.eat(target)


class EatenFoodRemover(WorldProcessor):
    def __init__(self):
        super(EatenFoodRemover, self).__init__()

    def process(self, world: World) -> None:
        world.food = [food_unit for food_unit in world.food if not food_unit.eaten]


class CorpseGrindingProcessor(WorldProcessor):
    def __init__(self):
        super(CorpseGrindingProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms:
            if not worm.dead:
                continue

            eaters = world.worms_at(worm.coordinates)
            for eater in eaters:
                if eater.dead:
                    continue
                eater.health += worm.level + worm.damage + worm.initiative
                eater.energy += (worm.level + worm.damage + worm.initiative) * 10


class DeadWormsRemover(WorldProcessor):
    def __init__(self):
        super(DeadWormsRemover, self).__init__()

    def process(self, world: World) -> None:
        alive_worms = [worm for worm in world.worms if not worm.dead]
        world.worms = alive_worms


class WormDivision(WorldProcessor):
    def __init__(self):
        super(WormDivision, self).__init__()

    def process(self, world: World) -> None:
        for parent in world.worms:
            if parent.divisions_limit > 0:
                child = Worm(parent.x, parent.y)
                child.genotype = parent.genotype
                child.family_affinity = parent.family_affinity + 0.00000000000001
                for gene in child.genotype:
                    child.genetical_boost(gene)
                world.worms.append(child)
                parent.divisions_limit -= 1
                child.generation = parent.generation + 1


class MutationProcessor(WorldProcessor):
    def __int__(self):
        super(MutationProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms:
            mutation_saving_throw = random.randint(1, 100)
            if mutation_saving_throw == 1:
                worm.substitution_mutation()
            elif 1 < mutation_saving_throw < 4:
                worm.insertion_mutation()
            elif 3 < mutation_saving_throw < 6:
                worm.deletion_mutation()


class TestAnalyticsProcessor(WorldProcessor):
    def __init__(self):
        super(TestAnalyticsProcessor, self).__init__()
        self.iterations = 0

    def process(self, world: World) -> None:
        self.iterations += 1
        print('iter', self.iterations)
        print('number of worms', len(world.worms))


if __name__ == "__main__":
    world = World(100, 100, 250, 1000)

    processors = [AgingProcessor(), ZeroEnergyProcessor(), PoisonProcessor(), MovementProcessor(), FightProcessor(),
                  CorpseGrindingProcessor(), DeadWormsRemover(),
                  FoodPickUpProcessor(), EatenFoodRemover(), AddFoodProcessor(),
                  LevelUpProcessor(), WormDivision(), MutationProcessor(),
                  TestAnalyticsProcessor(), Visualizer()]

    while True:
        for proc in processors:
            proc.process(world)
