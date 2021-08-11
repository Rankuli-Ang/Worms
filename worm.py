import random
from enum import Enum
from operator import add

from common_types import Cell


class Genes(Enum):
    ENERGY = 20
    HEALTH = 3
    DAMAGE = 2
    DEFENSE = 0.1


genes_variations = [Genes.HEALTH, Genes.DAMAGE, Genes.ENERGY, Genes.DEFENSE]


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


class Genetics:
    def __init__(self):
        self.genotype: list = []
        self.family_affinity: float = random.random()
        self.energetic_genes_pool: int = 0
        self.health_genes_pool: int = 0
        self.damage_genes_pool: int = 0
        self.defense_genes_pool: int = 0
        self.energetic_boost: int = 0
        self.health_boost: int = 0
        self.damage_boost: int = 0
        self.defense_boost: int = 0

    def create_genome(self):
        genotype = []
        genes_for_add = 12
        while genes_for_add > 0:
            genotype.append(random.choice(genes_variations))
            genes_for_add -= 1
        return genotype

    def insertion_mutation(self, inserted_gene: Genes) -> None:
        self.genotype.append(inserted_gene)

    def deletion_mutation(self, deleted_gene: Genes) -> None:
        self.genotype.remove(deleted_gene)

    def substitution_mutation(self, deleted_gene: Genes, inserted_gene: Genes) -> None:
        self.deletion_mutation(deleted_gene)
        self.insertion_mutation(inserted_gene)


class Character:
    def __init__(self, coordinates: tuple):
        self.coordinates = coordinates


class Food(Character):
    def __init__(self, coordinates: tuple):
        super().__init__(coordinates)
        self.nutritional_value: int = random.randint(1, 5)

    @property
    def eaten(self) -> bool:
        return self.nutritional_value <= 0


class Worm(Character):
    def __init__(self, coordinates: tuple):
        super().__init__(coordinates)
        self._name: str = random.choice(worms_names)
        self._health: int = random.randint(6, 9)
        self._damage: int = random.randint(1, 3)
        self._defense: float = random.uniform(0.8, 0.95)
        self._initiative: int = random.randint(1, 3)
        self._energy: int = 100
        self._level: int = 1
        self._experience: int = 0
        self._poisoned: int = 0
        self._divisions_limit: int = 0
        self._generation: int = 0
        self._age: int = 0

        self.genetics = Genetics()

    def get_health(self) -> int:
        return self._health

    def set_health(self, x) -> None:
        assert x is int or float, 'setting health is not number'
        self._health = x

    health = property(get_health, set_health)

    def get_damage(self) -> int:
        return self._damage

    def set_damage(self, x) -> None:
        assert x is int or float, 'setting damage is not number'
        self._damage = x

    damage = property(get_damage, set_damage)

    def get_defense(self) -> float:
        return self._defense

    def get_initiative(self) -> int:
        return self._initiative

    def get_energy(self) -> int:
        return self._energy

    def set_energy(self, x) -> None:
        assert x is int or float, 'setting energy is not number'
        self._energy = x

    energy = property(get_energy, set_energy)

    def get_level(self) -> int:
        return self._level

    def get_poisoned(self) -> int:
        return self._poisoned

    def set_poisoned(self, x) -> None:
        assert x is int or float, 'setting poisoned is not number'
        self._poisoned = x

    poisoned = property(get_poisoned, set_poisoned)

    def get_generation(self) -> int:
        return self._generation

    def get_divisions_limit(self) -> int:
        return self._divisions_limit

    def set_divisions_limit(self, x) -> None:
        assert x is int or float, 'setting divisions limit is not number'
        self._divisions_limit = x

    divisions_limit = property(get_divisions_limit, set_divisions_limit)

    def get_age(self) -> int:
        return self._age

    def set_age(self, x) -> None:
        assert x is int or float, 'setting age is not number'
        self._age = x

    age = property(get_age, set_age)

    def describe(self) -> None:
        print(f'Worm {self._name}:')
        print(f'\thealth {self._health}')
        print(f'\tenergy {self._energy}')
        print(f'\tdamage {self._damage}')
        print(f'\tdefense {self._defense}')
        print(f'\tinitiative {self._initiative}')
        print(f'\tlevel {self._level}')
        print(f'\texperience {self._experience}')
        print(f'\tpoisoned {self._poisoned}')
        print(f'\tgeneration {self._generation}')
        print(f'\tdivisions_number {self._divisions_limit}')

    def energetic_genes_realization(self) -> None:
        while self.genetics.energetic_genes_pool >= 3:
            self._energy += Genes.ENERGY.value
            self.genetics.energetic_genes_pool -= 3
            self.genetics.energetic_boost += 1
        if self.genetics.energetic_genes_pool < 0:
            self._energy -= Genes.ENERGY.value
            self.genetics.energetic_genes_pool += 3
            self.genetics.energetic_boost -= 1

    def health_genes_realization(self) -> None:
        while self.genetics.health_genes_pool >= 4:
            self._health += Genes.HEALTH.value
            self.genetics.health_genes_pool -= 4
            self.genetics.health_boost += 1
        if self.genetics.health_genes_pool < 0:
            self._health -= Genes.HEALTH.value
            self.genetics.health_genes_pool += 4
            self.genetics.health_boost -= 1

    def damage_genes_realization(self) -> None:
        while self.genetics.damage_genes_pool >= 5:
            self._damage += Genes.DAMAGE.value
            self.genetics.damage_genes_pool -= 5
            self.genetics.damage_boost += 1
        if self.genetics.damage_genes_pool < 0:
            self._damage -= Genes.DAMAGE.value
            self.genetics.damage_genes_pool += 5
            self.genetics.damage_boost -= 1

    def defense_genes_realization(self) -> None:
        while self.genetics.defense_genes_pool >= 5:
            self._defense -= Genes.DEFENSE.value
            if self._defense < 0.2:
                self._defense = 0.2
            self.genetics.defense_genes_pool -= 5
            self.genetics.defense_boost += 1
        if self.genetics.defense_genes_pool < 0:
            self._defense += Genes.DEFENSE.value
            self.genetics.defense_genes_pool += 5
            self.genetics.defense_boost -= 1

    def newborn_genetics_boost(self, genotype: list) -> None:
        for gene in genotype:
            if gene is Genes.ENERGY:
                self.genetics.energetic_genes_pool += 1
                continue
            if gene is Genes.HEALTH:
                self.genetics.health_genes_pool += 1
                continue
            if gene is Genes.DAMAGE:
                self.genetics.damage_genes_pool += 1
                continue
            if gene is Genes.DEFENSE:
                self.genetics.defense_genes_pool += 1

        self.energetic_genes_realization()
        self.health_genes_realization()
        self.damage_genes_realization()
        self.defense_genes_realization()

    def insertion_mutation(self) -> None:
        inserted_gene = random.choice(genes_variations)
        self.genetics.insertion_mutation(inserted_gene)
        if inserted_gene is Genes.ENERGY:
            self.genetics.energetic_genes_pool += 1
            self.energetic_genes_realization()
            return
        if inserted_gene is Genes.HEALTH:
            self.genetics.health_genes_pool += 1
            self.health_genes_realization()
            return
        if inserted_gene is Genes.DAMAGE:
            self.genetics.damage_genes_pool += 1
            self.damage_genes_realization()
            return
        if inserted_gene is Genes.DEFENSE:
            self.genetics.defense_genes_pool += 1
            self.defense_genes_realization()

    def deletion_mutation(self) -> None:
        deleted_gene = random.choice(self.genetics.genotype)
        if len(self.genetics.genotype) <= 1:
            self._health = 0
            return
        else:
            self.genetics.deletion_mutation(deleted_gene)
            if deleted_gene == Genes.ENERGY:
                self.genetics.energetic_genes_pool -= 1
                self.energetic_genes_realization()
                return
            if deleted_gene == Genes.HEALTH:
                self.genetics.health_genes_pool -= 1
                self.health_genes_realization()
                return
            if deleted_gene == Genes.DAMAGE:
                self.genetics.damage_genes_pool -= 1
                self.damage_genes_realization()
                return
            if deleted_gene == Genes.DEFENSE:
                self.genetics.defense_genes_pool -= 1
                self.defense_genes_realization()

    def substitution_mutation(self) -> None:
        self.deletion_mutation()
        self.insertion_mutation()

    def mutation_metamorphosis(self, mutation: str) -> None:
        if mutation == 'substitution_mutation':
            self.substitution_mutation()
            return
        elif mutation == 'insertion_mutation':
            self.insertion_mutation()
            return
        elif mutation == 'deletion_mutation':
            self.deletion_mutation()

    def level_up(self) -> None:
        if self.dead:
            return
        if self._experience < self._level + 2:
            return

        self._level += 1
        self._experience = 0

        level_ups = [self.level_up_damage, self.level_up_initiative]
        if self._defense > 0.2:
            level_ups.append(self.level_up_defense)

        level_up_func = random.choice(level_ups)
        level_up_func()

        if self._defense <= 0.2:
            self._defense = 0.2

        self.division_potential()

    def level_up_damage(self) -> int:
        self._damage += 2
        self._health += self._level // 3 + 3
        return self._damage

    def level_up_defense(self) -> float:
        self._defense -= self._level / 150 + 0.05
        self._health += self._level // 3 + 3
        return self._defense

    def level_up_initiative(self) -> int:
        self._initiative += 1
        self._health += self._level // 3 + 3
        return self._initiative

    def division_potential(self) -> None:
        if self._level > 2:
            self._divisions_limit += 1

    @property
    def dead(self) -> bool:
        return self._health <= 0

    def aging_factor(self) -> int:
        if self._age > 100:
            return 3
        elif self._age > 50:
            return 2
        else:
            return 1

    def poison(self, target) -> None:
        target.poisoned += random.randint(1, 3)

    def is_relative_to(self, other) -> bool:
        return abs(self.genetics.family_affinity - other.genetics.family_affinity) < 1e-12

    def is_dangerous(self, other_value: int) -> bool:
        return other_value > self._health

    def max_danger_at_location(self, worms_here: list):
        if len(worms_here) > 0:
            return max([worm.get_health() for worm in worms_here])
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
        if not self.dead and self._energy > 0:
            other.health -= self._damage * other.get_defense()
            self._experience += 1
            self._energy -= 2 * self.aging_factor()
            saving_throw = random.randint(1, 10)
            if saving_throw <= 3:
                self.poison(other)

    def eat(self, target_food) -> None:
        if not self.dead:
            if target_food.nutritional_value > 0:
                self._health += target_food.nutritional_value
                self._energy += target_food.nutritional_value * 5
                target_food.nutritional_value = 0
                if self._energy > 150:
                    self._divisions_limit += 1
                    self._energy -= 50

    def move(self, step: tuple, border_x: int, border_y: int) -> None:
        if not self.dead and self._energy > 0:
            new_coordinates = tuple(map(add, step, self.coordinates))
            new_x = min(max(new_coordinates[0], 0), border_x - 1)
            new_y = min(max(new_coordinates[1], 0), border_y - 1)
            self.coordinates = Cell(new_x, new_y)


if __name__ == "__main__":
    worm = Worm((10, 10))
    print(worm.health)
    worm.health -= 2
    print(worm.health)
