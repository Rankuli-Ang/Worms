import random


def read_names(filename):
    worms_names = []
    with open(filename, 'r') as reader:
        for line in reader:
            worms_names.append(line.rstrip('\n'))
    return worms_names


worms_names = read_names("Names.txt")


class Role:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y


class Food(Role):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.nutritional_value: int = random.randint(1, 5)

    @property
    def eaten(self) -> bool:
        return self.nutritional_value <= 0


class Worm(Role):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name: str = random.choice(worms_names)
        self.x: int = x
        self.y: int = y
        self.health: int = random.randint(6, 9)
        self.energy: int = 100
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.8, 0.95)
        self.initiative: int = random.randint(1, 3)
        self.level: int = 1
        self.experience: int = 0
        self.poisoned: int = 0
        self.genotype: float = random.random()
        self.generation: int = 0
        self.divisions_limit: int = 0
        self.age: int = 0

    def describe(self) -> None:
        print(f'Worm {self.name}:')
        print(f'\thealth {self.health}')
        print(f'\tenergy {self.energy}')
        print(f'\tdamage {self.damage}')
        print(f'\tdefense {self.defense}')
        print(f'\tinitiative {self.initiative}')
        print(f'\tlevel {self.level}')
        print(f'\texperience {self.experience}')
        print(f'\tpoisoned {self.poisoned}')
        print(f'\tgenotype {self.genotype}')
        print(f'\tgeneration {self.generation}')
        print(f'\tdivisions_number {self.divisions_limit}')

    def level_up(self) -> None:
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

        self.division_potential()

    def level_up_damage(self) -> int:
        self.damage += 2
        self.health += self.level // 3 + 3
        return self.damage

    def level_up_defense(self) -> float:
        self.defense -= self.level / 150 + 0.05
        self.health += self.level // 3 + 3
        return self.defense

    def level_up_initiative(self) -> int:
        self.initiative += 1
        self.health += self.level // 3 + 3
        return self.initiative

    def division_potential(self) -> None:
        if self.level > 2:
            self.divisions_limit += 1

    @property
    def dead(self) -> bool:
        return self.health <= 0

    def aging_factor(self) -> int:
        if self.age > 100:
            return 3
        elif self.age > 50:
            return 2
        else:
            return 1

    def poison(self, target) -> None:
        target.poisoned += random.randint(1, 3)

    def is_relative_to(self, other) -> bool:
        return abs(self.genotype - other.genotype) < 1e-12

    def is_dangerous(self, other_value: int) -> bool:
        return other_value > self.health

    def get_safe_steps(self, locations: dict) -> list:
        safe_steps = []
        for location in locations:
            max_health_in_location = locations.setdefault(location)
            if self.is_dangerous(max_health_in_location) is False:
                safe_steps.append(location.value)
        return safe_steps

    def get_best_steps(self, safe_steps: list, steps_with_food: list) -> list:
        best_steps = []
        for step in steps_with_food:
            if step in safe_steps:
                best_steps.append(step)
        if len(best_steps) > 0:
            return best_steps
        else:
            return safe_steps



    def strike(self, other) -> None:
        if not self.dead and self.energy > 0:
            other.health -= self.damage * other.defense
            self.experience += 1
            self.energy -= 2 * self.aging_factor()
            saving_throw = random.randint(1, 10)
            if saving_throw <= 3:
                self.poison(other)

    def eat(self, target_food) -> None:
        if not self.dead:
            if target_food.nutritional_value > 0:
                self.health += target_food.nutritional_value
                self.energy += target_food.nutritional_value * 5
                target_food.nutritional_value = 0
                if self.energy > 120:
                    self.divisions_limit += 1
                    self.energy -= 20

    def move(self, dx: int, dy: int, border_x: int, border_y: int) -> None:
        if not self.dead and self.energy > 0:
            assert abs(dx) + abs(dy) == 1
            self.x += dx
            self.y += dy

            self.y = min(max(self.y, 0), border_y - 1)
            self.x = min(max(self.x, 0), border_x - 1)
            self.energy -= 1 * self.aging_factor()
