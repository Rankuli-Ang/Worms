import random
from typing import List

import cv2
import numpy as np

from worm import Role, Worm, Food


# from opencv import * # плохой тон

# import opencv
# class Home(opencv.Role)

class Home(Role):
    def __init__(self):
        super().__init__(0, 0)


class World:
    def __init__(self):
        self.worms: List[Worm] = []
        self.food: List[Food] = []
        self.name: str = 'World'

        self.height = 100
        self.width = 100

    @property
    def worms_by_initiative(self) -> List[Worm]:
        worms_by_initiative = world.worms
        worms_by_initiative.sort(key=lambda worm: worm.initiative)
        return worms_by_initiative

    def worms_at(self, x: int, y: int) -> List[Worm]:
        return [worm for worm in self.worms if worm.coordinate_y == y and worm.coordinate_x == x]


def populate_world(world: World, worms_num: int = 100) -> None:
    for i in range(worms_num):
        worm = Worm(random.randint(0, world.width), random.randint(0, world.height))
        world.worms.append(worm)


class WorldProcessor:
    def __init__(self):
        pass

    def process(self, world: World) -> None:
        pass


class Visualizer(WorldProcessor):
    def __init__(self):
        super(Visualizer, self).__init__()

        self._color_worm = (255, 255, 255)
        self._color_space = (0, 0, 0)
        self._color_food = (0, 0, 255)

    def process(self, world: World) -> None:
        vis = np.zeros((world.height, world.width, 3), dtype='uint8')

        for worm in world.worms:
            vis[worm.coordinate_y, worm.coordinate_x] = self._color_worm

        scale = 4
        vis = cv2.resize(vis, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

        cv2.imshow('vis', vis)
        cv2.waitKey(1)


class MovementProcessor(WorldProcessor):
    def __init__(self):
        super(MovementProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            dcoord = random.choice(movements)
            worm.move(dcoord[0], dcoord[1], world.width, world.height)


class FightProcessor(WorldProcessor):
    def __init__(self):
        super(FightProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms_by_initiative:
            targets = world.worms_at(worm.coordinate_x, worm.coordinate_y)
            target = random.choice(targets)

            if target is worm:
                continue

            worm.strike(target)
            target.strike(worm)


class LevelUpProcessor(WorldProcessor):
    def __init__(self):
        super(LevelUpProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms:
            worm.level_up()


class CorpseGrindingProcessor(WorldProcessor):
    def __init__(self):
        super(CorpseGrindingProcessor, self).__init__()

    def process(self, world: World) -> None:
        for worm in world.worms:
            if not worm.dead:
                continue

            eaters = world.worms_at(worm.coordinate_x, worm.coordinate_y)
            for eater in eaters:
                if eater.dead:
                    continue
                eater.health += worm.level


class DeadWormsRemover(WorldProcessor):
    def __init__(self):
        super(DeadWormsRemover, self).__init__()

    def process(self, world: World) -> None:
        alive_worms = [worm for worm in world.worms if not worm.dead]
        world.worms = alive_worms


if __name__ == "__main__":
    world = World()
    populate_world(world, 1000)

    processors = [MovementProcessor(), FightProcessor(), CorpseGrindingProcessor(), DeadWormsRemover(),
                  LevelUpProcessor(), Visualizer()]

    while True:
        for proc in processors:
            proc.process(world)
