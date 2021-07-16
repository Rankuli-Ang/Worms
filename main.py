import random
from typing import List

import cv2
import numpy as np

from worm import Role, Worm, Food

iterations = 0


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

    def food_at(self, x: int, y: int) -> List[Food]:
        return [food_unit for food_unit in self.food if food_unit.coordinate_x == x and food_unit.coordinate_y == y]

    def cell_scanning(self, x: int, y: int):
        max_health_enemy = 0
        food_presense = 'no'
        for worm in self.worms:
            if worm.coordinate_y == y and worm.coordinate_x == x:
                if worm.health > max_health_enemy:
                    max_health_enemy = worm.health
        for food_unit in self.food:
            if food_unit.coordinate_x == x and food_unit.coordinate_y == y:
                food_presense = 'yes'
        cell = {'food': food_presense, 'max_health_enemy': max_health_enemy, 'coordinates': (x, y)}
        return cell

    def test_new_save_location(self, x: int, y: int, reference_health: int):
        selected_ways = []
        best_ways = []
        '''best_choice_is_not_to_move = (x, y)'''
        up = self.cell_scanning(x, y - 1)
        down = self.cell_scanning(x, y + 1)
        left = self.cell_scanning(x - 1, y)
        right = self.cell_scanning(x + 1, y)
        variations = [up, down, left, right]
        for variation in variations:
            if variation.get('max_health_enemy') < reference_health:
                selected_ways.append(variation.get('coordinates'))
                if variation.get('food') == 'yes':
                    best_ways.append(variation.get('coordinates'))

        if len(best_ways) > 0:
            final_best_ways = []
            for (c, v) in best_ways:
                (c, v) = (x - c, y - v)
                final_best_ways.append((c, v))
            return final_best_ways
        else:
            final_selected_ways = []
            for (c, v) in selected_ways:
                (c, v) = (x - c, y - v)
                final_selected_ways.append((c, v))
            return final_selected_ways

    def search_food_nearby(self, x: int, y: int) -> list[tuple[int, int]]:
        variations = {(0, -1): len(list(world.food_at(x, y - 1))),
                      (1, 0): len(list(world.food_at(x + 1, y))),
                      (0, 1): len(list(world.food_at(x, y + 1))),
                      (-1, 0): len(list(world.food_at(x - 1, y)))}
        max_value = max(variations.values())

        return [key for key in variations.keys() if variations[key] == max_value]

    def search_location_with_enemy(self, x: int, y: int):
        variations = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
        return [(c, v) for (c, v) in variations for worm in self.worms if worm.coordinate_y == c and
                worm.coordinate_x == v]

    def search_save_location_nearby(self, x: int, y: int, reference_health: int):
        locations_with_enemy = world.search_location_with_enemy(x, y)
        safe_location = {(x, y - 1): (0, -1), (x + 1, y): (1, 0), (x, y + 1): (0, 1), (x - 1, y): (-1, 0)}
        for (c, v) in locations_with_enemy:
            enemy_in = world.worms_at(c, v)
            for enemy in enemy_in:
                if enemy.health > reference_health:
                    if enemy.energy > 0:
                        if (c, v) in safe_location.keys():
                            safe_location.pop((c, v))
        safe = list(safe_location.values())
        return safe


def populate_world(world: World, worms_num: int = 100) -> None:
    for i in range(worms_num):
        worm = Worm(random.randrange(0, world.width), random.randrange(0, world.height))
        world.worms.append(worm)


def sow_food(world: World, food_num: int = 10) -> None:
    for i in range(food_num):
        food_unit = Food(random.randrange(0, world.width), random.randrange(0, world.height))
        world.food.append(food_unit)


class WorldProcessor:
    def __init__(self):
        pass

    def process(self, world: World) -> None:
        pass


class Visualizer(WorldProcessor):
    def __init__(self):
        super(Visualizer, self).__init__()

        self._color_worm_generation_0 = (255, 255, 255)
        self._color_worm_generation_1 = (255, 0, 0)
        self._color_worm_generation_2 = (0, 255, 0)
        self._color_worm_generation_3 = (0, 255, 255)
        self._color_space = (0, 0, 0)
        self._color_food = (0, 0, 255)

    def process(self, world: World) -> None:
        vis = np.zeros((world.height, world.width, 3), dtype='uint8')
        worm_color = [self._color_worm_generation_0, self._color_worm_generation_1, self._color_worm_generation_2,
                      self._color_worm_generation_3]
        for worm in world.worms:
            if worm.generation < 4:
                vis[worm.coordinate_y, worm.coordinate_x] = worm_color[worm.generation]
            else:
                vis[worm.coordinate_y, worm.coordinate_x] = self._color_worm_generation_0

        for food_unit in world.food:
            vis[food_unit.coordinate_y, food_unit.coordinate_x] = self._color_food

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
            if not worm.dead:
                enemies = [enemy for enemy in world.worms_at(worm.coordinate_x, worm.coordinate_y) if enemy is not worm]
                if len(enemies) > 0:
                    for enemy in enemies:
                        if worm.is_dangerous_here(enemy):
                            danger_free_movements = world.test_new_save_location(worm.coordinate_x, worm.coordinate_y,
                                                                                 worm.health)
                            if len(danger_free_movements) == 0:
                                break
                            else:
                                dcoord = random.choice(danger_free_movements)
                                worm.move(dcoord[0], dcoord[1], world.width, world.height)
                                break
                else:
                    targets = world.food_at(worm.coordinate_x, worm.coordinate_y)
                    if len(targets) != 0:
                        continue
                    else:
                        danger_free_movements = world.test_new_save_location(worm.coordinate_x, worm.coordinate_y,
                                                                             worm.health)
                        if len(danger_free_movements) == 0:
                            continue
                        else:
                            dcoord = random.choice(danger_free_movements)
                            worm.move(dcoord[0], dcoord[1], world.width, world.height)
                            continue


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
            targets = world.worms_at(worm.coordinate_x, worm.coordinate_y)
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
            targets = world.food_at(eater.coordinate_x, eater.coordinate_y)
            if len(targets) != 0:
                target = random.choice(targets)
                eater.eat(target)


class EatenFoodRemover(WorldProcessor):
    def __init__(self):
        super(EatenFoodRemover, self).__init__()

    def process(self, world: World) -> None:
        leftover_food = [food_unit for food_unit in world.food if not food_unit.eaten]
        world.food = leftover_food


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
                child = Worm(parent.coordinate_x, parent.coordinate_y)
                child.genotype = parent.genotype + 0.00000000000001
                world.worms.append(child)
                parent.divisions_limit -= 1
                child.generation = parent.generation + 1


class TestAnalyticsProcessor(WorldProcessor):
    def __init__(self):
        super(TestAnalyticsProcessor, self).__init__()

    def process(self, world: World) -> None:
        global iterations
        iterations += 1
        print('iter', iterations)
        print('number of worms', len(world.worms))


if __name__ == "__main__":
    world = World()
    populate_world(world, 500)
    sow_food(world, 1000)

    processors = [AgingProcessor(), ZeroEnergyProcessor(), PoisonProcessor(), MovementProcessor(), FightProcessor(),
                  CorpseGrindingProcessor(), DeadWormsRemover(),
                  FoodPickUpProcessor(), EatenFoodRemover(), AddFoodProcessor(),
                  LevelUpProcessor(), WormDivision(),
                  TestAnalyticsProcessor(), Visualizer()]

    while True:
        for proc in processors:
            proc.process(world)
