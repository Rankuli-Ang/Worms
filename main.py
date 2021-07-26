import random
from typing import List
from enum import Enum

import cv2
import numpy as np

from worm import Worm, Food


class Neighbors(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


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
            worm = Worm(random.randrange(0, self.width), random.randrange(0, self.height))
            self.worms.append(worm)

    def sow_food(self, food_num: int = 1000):
        for i in range(food_num):
            food_unit = Food(random.randrange(0, self.width), random.randrange(0, self.height))
            self.food.append(food_unit)

    @property
    def worms_by_initiative(self) -> List[Worm]:
        return sorted(world.worms, key=lambda worm: worm.initiative)

    def worms_at(self, x: int, y: int) -> List[Worm]:
        return [worm for worm in self.worms if worm.y == y and worm.x == x]

    def food_at(self, x: int, y: int) -> List[Food]:
        return [food_unit for food_unit in self.food if food_unit.x == x and food_unit.y == y]

    def max_danger_here(self, x: int, y: int) -> int:
        max_danger = 0
        worms_at_location = world.worms_at(x, y)
        if len(worms_at_location) > 0:
            return max([worm.health for worm in world.worms_at(x, y)])
        else:
            return 0

    def get_max_danger_neighbours(self, x: int, y: int) -> dict:
        max_danger_neighbours = {Neighbors.UP: world.max_danger_here(x, y - 1),
                                 Neighbors.RIGHT: world.max_danger_here(x + 1, y),
                                 Neighbors.DOWN: world.max_danger_here(x, y + 1),
                                 Neighbors.LEFT: world.max_danger_here(x - 1, y)}
        return max_danger_neighbours

    def get_neighbours_with_food(self, x: int, y: int) -> list:
        neighbours_with_food = []
        neighbours = {Neighbors.UP: world.food_at(x, y - 1),
                      Neighbors.RIGHT: world.food_at(x + 1, y),
                      Neighbors.DOWN: world.food_at(x, y + 1),
                      Neighbors.LEFT: world.food_at(x - 1, y)}
        for neighbour in neighbours:
            location = neighbours.setdefault(neighbour)
            if len(location) != 0:
                neighbours_with_food.append(neighbour.value)
        return neighbours_with_food


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
                vis[worm.coordinates[1], worm.coordinates[0]] = worm_color[worm.generation].value
                '''vis[worm.y, worm.x] = worm_color[worm.generation].value'''
            else:
                '''vis[worm.y, worm.x] = Colors.WHITE.value'''
                vis[worm.coordinates[1], worm.coordinates[0]] = Colors.WHITE.value

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

            enemies = [enemy for enemy in world.worms_at(worm.x, worm.y) if enemy is not worm]
            if len(enemies) == 0:
                targets = world.food_at(worm.x, worm.y)
                if len(targets) > 0:
                    continue
                else:
                    max_danger_neighbours = world.get_max_danger_neighbours(worm.x, worm.y)
                    safe_steps = worm.get_safe_steps(max_danger_neighbours)
                    if len(safe_steps) > 0:
                        steps_with_food = world.get_neighbours_with_food(worm.x, worm.y)
                        dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))
                        worm.moving(dcoord, world.width, world.height)
                        '''worm.move(dcoord[0], dcoord[1], world.width, world.height)'''
            else:
                danger = world.max_danger_here(worm.x, worm.y)
                if not worm.is_dangerous(danger):
                    continue
                else:
                    max_danger_neighbours = world.get_max_danger_neighbours(worm.x, worm.y)
                    safe_steps = worm.get_safe_steps(max_danger_neighbours)
                    if len(safe_steps) == 0:
                        continue
                    else:
                        steps_with_food = world.get_neighbours_with_food(worm.x, worm.y)
                        dcoord = random.choice(worm.get_best_steps(safe_steps, steps_with_food))
                        worm.moving(dcoord, world.width, world.height)
                        '''worm.move(dcoord[0], dcoord[1], world.width, world.height)'''


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
            targets = world.worms_at(worm.x, worm.y)
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
            targets = world.food_at(eater.x, eater.y)
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

            eaters = world.worms_at(worm.x, worm.y)
            for eater in eaters:
                if eater.dead:
                    continue
                eater.health += worm.level + worm.damage + worm.initiative
                eater.energy += (worm.level + worm.damage + worm.initiative) * 5


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
                child.genotype = parent.genotype + 0.00000000000001
                world.worms.append(child)
                parent.divisions_limit -= 1
                child.generation = parent.generation + 1


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
                  LevelUpProcessor(), WormDivision(),
                  TestAnalyticsProcessor(), Visualizer()]

    while True:
        for proc in processors:
            proc.process(world)
