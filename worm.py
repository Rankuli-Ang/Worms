import random
from enum import Enum
from collections import namedtuple


class Genes(Enum):
    ENERGY = 20
    HEALTH = 3
    DAMAGE = 2
    DEFENSE = 0.1


genes_variations = [Genes.HEALTH, Genes.DAMAGE, Genes.ENERGY, Genes.DEFENSE]

cell = namedtuple('Cell', ['x', 'y'])


class Neighbors(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def create_genome():
    genotype = []
    genes_for_add = 12
    while genes_for_add > 0:
        genotype.append(random.choice(genes_variations))
        genes_for_add -= 1
    return genotype


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
        self.coordinates = cell(x, y)


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
        self.health: int = random.randint(6, 9)
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.8, 0.95)
        self.initiative: int = random.randint(1, 3)
        self.energy: int = 100
        self.level: int = 1
        self.experience: int = 0
        self.poisoned: int = 0
        self.family_affinity: float = random.random()
        self.divisions_limit: int = 0
        self.generation: int = 0
        self.divisions_limit: int = 0
        self.age: int = 0
        'genetics'
        self.genotype: list = []
        self.energetic_genes_pool: int = 0
        self.health_genes_pool: int = 0
        self.damage_genes_pool: int = 0
        self.defense_genes_pool: int = 0
        self.energetic_boost: int = 0
        self.health_boost: int = 0
        self.damage_boost: int = 0
        self.defense_boost: int = 0

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
        print(f'\tgenotype {self.family_affinity}')
        print(f'\tgeneration {self.generation}')
        print(f'\tdivisions_number {self.divisions_limit}')

    def energetic_genes_score(self) -> None:
        if self.energetic_genes_pool >= 3:
            self.energy += Genes.ENERGY.value
            self.energetic_genes_pool -= 3
            self.energetic_boost += 1
        if self.energetic_genes_pool < 0:
            self.energy -= Genes.ENERGY.value
            self.energetic_genes_pool += 3
            self.energetic_boost -= 1

    def health_genes_score(self) -> None:
        if self.health_genes_pool >= 4:
            self.health += Genes.HEALTH.value
            self.health_genes_pool -= 4
            self.health_boost += 1
        if self.health_genes_pool < 0:
            self.health -= Genes.HEALTH.value
            self.health_genes_pool += 4
            self.health_boost -= 1

    def damage_genes_score(self) -> None:
        if self.damage_genes_pool >= 5:
            self.damage += Genes.DAMAGE.value
            self.damage_genes_pool -= 5
            self.damage_boost += 1
        if self.damage_genes_pool < 0:
            self.damage -= Genes.DAMAGE.value
            self.damage_genes_pool += 5
            self.damage_boost -= 1

    def defense_genes_score(self) -> None:
        if self.defense_genes_pool >= 5:
            self.defense -= Genes.DEFENSE.value
            if self.defense < 0.2:
                self.defense = 0.2
            self.defense_genes_pool -= 5
            self.defense_boost += 1
        if self.defense_genes_pool < 0:
            self.defense += Genes.DEFENSE.value
            self.defense_genes_pool += 5
            self.defense_boost -= 1

    def genetical_boost(self, gene: Genes) -> None:
        if gene is Genes.ENERGY:
            self.energetic_genes_pool += 1
            self.energetic_genes_score()
        if gene is Genes.HEALTH:
            self.health_genes_pool += 1
            self.health_genes_score()
        if gene is Genes.DAMAGE:
            self.damage_genes_pool += 1
            self.damage_genes_score()
        if gene is Genes.DEFENSE:
            self.defense_genes_pool += 1
            self.defense_genes_score()

    def insertion_mutation(self) -> None:
        inserted_gene = random.choice(genes_variations)
        self.genotype.append(inserted_gene)
        self.genetical_boost(inserted_gene)

    def deletion_mutation(self) -> None:
        deleted_gene = random.choice(self.genotype)
        if len(self.genotype) > 1:
            self.genotype.remove(deleted_gene)
            if deleted_gene == Genes.ENERGY:
                self.energetic_genes_pool -= 1
                self.energetic_genes_score()
            if deleted_gene == Genes.HEALTH:
                self.health_genes_pool -= 1
                self.health_genes_score()
            if deleted_gene == Genes.DAMAGE:
                self.damage_genes_pool -= 1
                self.damage_genes_score()
            if deleted_gene == Genes.DEFENSE:
                self.defense_genes_pool -= 1
                self.defense_genes_score()
        else:
            self.health = 0

    def substitution_mutation(self) -> None:
        self.deletion_mutation()
        self.insertion_mutation()

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
        return abs(self.family_affinity - other.family_affinity) < 1e-12

    def is_dangerous(self, other_value: int) -> bool:
        return other_value > self.health

    def max_danger_at_location(self, worms_here: list):
        if len(worms_here) > 0:
            return max([worm.health for worm in worms_here])
        else:
            return 0

    def get_safe_steps(self, steps: dict) -> list:
        safe_steps = []
        for step in steps:
            if not self.is_dangerous(self.max_danger_at_location(steps.get(step))):
                safe_steps.append(step.value)
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
                if self.energy > 150:
                    self.divisions_limit += 1
                    self.energy -= 50

    def move(self, step: tuple, border_x: int, border_y: int) -> None:
        if not self.dead and self.energy > 0:
            new_x = min(max(step[0] + self.coordinates.__getattribute__('x'), 0), border_x - 1)
            new_y = min(max(step[1] + self.coordinates.__getattribute__('y'), 0), border_y - 1)
            self.coordinates = cell(new_x, new_y)
