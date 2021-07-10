import random


def read_names(filename):
    worms_names = []
    with open(filename, 'r') as reader:
        for line in reader:
            worms_names.append(line.rstrip('\n'))
    return worms_names


worms_names = read_names("Names.txt")


class Role:
    def __init__(self, coordinate_x, coordinate_y):
        self.coordinate_x: int = coordinate_x
        self.coordinate_y: int = coordinate_y


class Food(Role):
    def __init__(self, coordinate_x, coordinate_y):
        super().__init__(coordinate_x, coordinate_y)
        self.coordinate_x: int = coordinate_x
        self.coordinate_y: int = coordinate_y
        self.nutritional_value: int = random.randint(1, 5)

    @property
    def eaten(self) -> bool:
        return self.nutritional_value <= 0


class Worm(Role):
    def __init__(self, coordinate_x, coordinate_y):
        super().__init__(coordinate_x, coordinate_y)
        self.name: str = random.choice(worms_names)
        self.coordinate_x: int = coordinate_x
        self.coordinate_y: int = coordinate_y
        self.health: int = random.randint(6, 9)
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.8, 0.95)
        self.initiative: int = random.randint(1, 3)
        self.level: int = 1
        self.experience: int = 0
        self.poisoned: int = 0

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
        if self.dead:
            return
        if self.experience < self.level + 2:
            return

        self.level += 1
        self.experience = 0

        level_ups = [self.level_up_damage, self.level_up_initiative]
        if self.defense >= 0.2:
            level_ups.append(self.level_up_defense)

        level_up_func = random.choice(level_ups)
        level_up_func()

        if self.defense <= 0.2:
            self.defense = 0.2

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

    @property
    def dead(self) -> bool:
        return self.health <= 0

    def poison(self, target):
        target.poisoned += random.randint(1, 3)

    def strike(self, other):
        if not self.dead:
            other.health -= self.damage * other.defense
            self.experience += 1
            saving_throw = random.randint(1, 10)
            if saving_throw <= 3:
                self.poison(other)

    def eat(self, target_food):
        if target_food.nutritional_value > 0:
            self.health += target_food.nutritional_value
            target_food.nutritional_value = 0

    def move(self, dx: int, dy: int, border_x: int, border_y: int) -> None:
        assert abs(dx) + abs(dy) == 1
        self.coordinate_x += dx
        self.coordinate_y += dy

        self.coordinate_y = min(max(self.coordinate_y, 0), border_y - 1)
        self.coordinate_x = min(max(self.coordinate_x, 0), border_x - 1)
