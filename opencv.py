import random

import cv2
import worms as wm

wm.worms_naming()
list_of_worms = []
list_of_food = []
world_image = cv2.imread('tabula_rasa.png')
world_height, world_width, world_channels = world_image.shape
world_coordinates = [[0] * 256 for i in range(256)]
world_name = 'World'
image_worms = [0, 0, 0]
image_space = [255, 255, 255]
image_food = [0, 0, 255]


# точки изображения - y,x; точки координат - x,y


def creating_worm(x, y):
    global list_of_worms
    world_image[y, x] = image_worms
    list_of_worms.append(worm(x, y))
    world_coordinates[x][y] = 1


def detecting_worm(x, y):
    for unit in list_of_worms:
        if unit.coordinate_x == x:
            if unit.coordinate_y == y:
                return unit


def creating_food(x, y):
    global list_of_food
    world_image[y, x] = image_food
    list_of_food.append(food(x, y))
    world_coordinates[x][y] = 'food'


def deleting_food(x, y):
    global list_of_food
    world_coordinates[x][y] = 0
    world_image[y, x] = image_space
    for deleting_one in list_of_food:
        if deleting_one.coordinate_x == x:
            if deleting_one.coordinate_y == y:
                list_of_food.remove(deleting_one)


def detecting_food(x, y):
    for feed in list_of_food:
        if feed.coordinate_x == x:
            if feed.coordinate_y == y:
                return feed


class filler:
    def __init__(self, coordinate_x, coordinate_y):
        self.coordinate_x: int = coordinate_x
        self.coordinate_y: int = coordinate_y

    def coordinates_check(self):
        print('Filler coordinates:')
        print(f'Coordinate_x: {self.coordinate_x}')
        print(f'Coordinate_y: {self.coordinate_y}')


class food(filler):
    def __init__(self, coordinate_x, coordinate_y):
        super().__init__(coordinate_x, coordinate_y)
        self.nutritional_value: int = random.randint(1, 5)


class worm(filler):
    def __init__(self, coordinate_x, coordinate_y):
        super().__init__(coordinate_x, coordinate_y)
        self.name: str = random.choice(wm.worms_names_list)
        self.coordinate_x: int = coordinate_x
        self.coordinate_y: int = coordinate_y
        self.health: int = random.randint(6, 9)
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.8, 0.95)
        self.initiative: int = random.randint(1, 3)
        self.level: int = 1
        self.experience: int = 0
        self.poisoned: int = 0
        self.already_dead: int = 0

    def describe(self):
        print(f'Worm {self.name}:')
        print(f'\thealth {self.health}')
        print(f'\tdamage {self.damage}')
        print(f'\tdefense {self.defense}')
        print(f'\tinitiative {self.initiative}')
        print(f'\tlevel {self.level}')
        print(f'\texperience {self.experience}')
        print(f'\tpoisoned {self.poisoned}')

    def level_up(self):
        if self.already_dead == 0:
            if self.experience >= self.level + 2:
                self.level += 1
                self.experience = 0
                level_ups = [self.level_up_damage(), self.level_up_initiative(), self.level_up_defense()]
                level_ups_without_def = [self.level_up_damage(), self.level_up_initiative()]
                print('BEFORE:', 'damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)
                if self.defense <= 0.2:
                    self.defense = 0.2
                    level_ups_value = random.choice(level_ups_without_def)
                    print('value', level_ups_value)
                    if level_ups_value == level_ups_without_def[0]:
                        self.level_up_damage()
                        print('damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)
                    else:
                        self.level_up_initiative()
                        print('damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)
                else:
                    level_ups_value = random.choice(level_ups)
                    print('value', level_ups_value)
                    if level_ups_value == level_ups[0]:
                        self.level_up_damage()
                        print('damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)
                    elif level_ups_value == level_ups[1]:
                        self.level_up_initiative()
                        print('damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)
                    else:
                        self.level_up_defense()
                        print('damage', self.damage, 'defense', self.defense, 'initiative', self.initiative)

    def level_up_damage(self):
        self.damage += 2
        self.health += self.level // 3 + 3
        return self.damage

    def level_up_defense(self):
        self.defense -= self.level / 150 + 0.05
        self.health += self.level // 3 + 3
        return self.defense

    def level_up_initiative(self):
        self.initiative += 1
        self.health += self.level // 3 + 3
        return self.initiative

    def is_dead(self):
        if self.health <= 0:
            self.already_dead += 1
            return self.already_dead

    def strike(self, other):
        if self.already_dead == 0:
            other.health -= self.damage * other.defense
            other.is_dead()
            self.experience += 1

    '''
    def poison_effect(self):
        if self.poisoned > 0:
            self.health -= 1
            self.poisoned -= 1'''

    def moving_up(self):
        if self.coordinate_y > 1:
            if world_coordinates[self.coordinate_x][self.coordinate_y - 1] == 1:
                enemy = detecting_worm(self.coordinate_x, self.coordinate_y - 1)
                if hasattr(enemy, 'health'):
                    self.strike(enemy)
                    enemy.strike(self)
                    self.level_up()
                    enemy.level_up()

            elif world_coordinates[self.coordinate_x][self.coordinate_y - 1] == 'food':
                feed = detecting_food(self.coordinate_x, self.coordinate_y - 1)
                self.health += feed.nutritional_value
                deleting_food(self.coordinate_x, self.coordinate_y - 1)

            else:
                world_image[self.coordinate_y, self.coordinate_x] = image_space
                world_coordinates[self.coordinate_x][self.coordinate_y] = 0
                self.coordinate_y -= 1
                world_image[self.coordinate_y, self.coordinate_x] = image_worms
                world_coordinates[self.coordinate_x][self.coordinate_y] = 1
        else:
            pass

    def moving_down(self):
        if self.coordinate_y < 12:
            if world_coordinates[self.coordinate_x][self.coordinate_y + 1] == 1:
                enemy = detecting_worm(self.coordinate_x, self.coordinate_y + 1)
                if hasattr(enemy, 'health'):
                    self.strike(enemy)
                    enemy.strike(self)
                    self.level_up()
                    enemy.level_up()

            elif world_coordinates[self.coordinate_x][self.coordinate_y + 1] == 'food':
                feed = detecting_food(self.coordinate_x, self.coordinate_y + 1)
                self.health += feed.nutritional_value
                deleting_food(self.coordinate_x, self.coordinate_y + 1)

            else:
                world_image[self.coordinate_y, self.coordinate_x] = image_space
                world_coordinates[self.coordinate_x][self.coordinate_y] = 0
                self.coordinate_y += 1
                world_image[self.coordinate_y, self.coordinate_x] = image_worms
                world_coordinates[self.coordinate_x][self.coordinate_y] = 1
        else:
            pass

    def moving_left(self):
        if self.coordinate_x > 1:
            if world_coordinates[self.coordinate_x - 1][self.coordinate_y] == 1:
                enemy = detecting_worm(self.coordinate_x - 1, self.coordinate_y)
                if hasattr(enemy, 'health'):
                    self.strike(enemy)
                    enemy.strike(self)
                    self.level_up()
                    enemy.level_up()

            elif world_coordinates[self.coordinate_x - 1][self.coordinate_y] == 'food':
                feed = detecting_food(self.coordinate_x - 1, self.coordinate_y)
                self.health += feed.nutritional_value
                deleting_food(self.coordinate_x - 1, self.coordinate_y)

            else:
                world_image[self.coordinate_y, self.coordinate_x] = image_space
                world_coordinates[self.coordinate_x][self.coordinate_y] = 0
                self.coordinate_x -= 1
                world_image[self.coordinate_y, self.coordinate_x] = image_worms
                world_coordinates[self.coordinate_x][self.coordinate_y] = 1
        else:
            pass

    def moving_right(self):
        if self.coordinate_x < 12:
            if world_coordinates[self.coordinate_x + 1][self.coordinate_y] == 1:
                enemy = detecting_worm(self.coordinate_x + 1, self.coordinate_y)
                if hasattr(enemy, 'health'):
                    self.strike(enemy)
                    enemy.strike(self)
                    self.level_up()
                    enemy.level_up()

            elif world_coordinates[self.coordinate_x + 1][self.coordinate_y] == 'food':
                feed = detecting_food(self.coordinate_x + 1, self.coordinate_y)
                self.health += feed.nutritional_value
                deleting_food(self.coordinate_x + 1, self.coordinate_y)
            else:
                world_image[self.coordinate_y, self.coordinate_x] = image_space
                world_coordinates[self.coordinate_x][self.coordinate_y] = 0
                self.coordinate_x += 1
                world_image[self.coordinate_y, self.coordinate_x] = image_worms
                world_coordinates[self.coordinate_x][self.coordinate_y] = 1
        else:
            pass


def corpsegrinding():
    global list_of_worms
    remains = 0
    alive_worms = []
    if len(list_of_worms) > 0:
        for alive in list_of_worms:
            if alive.already_dead == 0:
                alive_worms.append(alive)
            else:
                world_image[alive.coordinate_y, alive.coordinate_x] = image_space
                world_coordinates[alive.coordinate_x][alive.coordinate_y] = 0
        corpses = (len(list_of_worms) - len(alive_worms))
        list_of_worms.clear()
        for come_back in alive_worms:
            list_of_worms.append(come_back)
        if corpses > 0:
            if len(list_of_worms) > 0:
                remains = corpses * 3 / len(list_of_worms)
                for eater in list_of_worms:
                    eater.health += remains
        return list_of_worms


# test
# state at the beginning
n = 0
while n < 10:
    creating_worm(1 + n, 1 + n)
    n += 1

k = 1
while k < 11:
    creating_food(2 + k, 1 + k)
    k += 1

m = 0
while m < 6:
    creating_food(m * 2, m)
    m += 1

cv2.imshow(world_name, world_image)
cv2.waitKey(0)

visualize_counter = 0
while len(list_of_worms) > 1:
    list_of_worms.sort(key=lambda worm: worm.initiative)
    visualize_counter += 1
    for unit in list_of_worms:
        moving_list = [1, 2, 3, 4]
        x = random.choice(moving_list)
        if x == 1:
            unit.moving_up()
        elif x == 2:
            unit.moving_down()
        elif x == 3:
            unit.moving_left()
        else:
            unit.moving_right()
        if visualize_counter == 25:
            cv2.imshow(world_name, world_image)
            cv2.waitKey(0)
            visualize_counter = 0
    corpsegrinding()

if len(list_of_worms) == 1:
    print(list_of_worms[0].describe())
else:
    print('All is Dead!')

print('end')
