import random
"""The module is used to randomize 
the initial characteristics of
 genetics, food, worms."""
from enum import Enum
from operator import add

from common_types import Cell


class Genes(Enum):
    """Stat bonus from genes."""
    ENERGY = 20
    HEALTH = 3
    DAMAGE = 2
    DEFENSE = 0.1


genes_variations = [Genes.HEALTH, Genes.DAMAGE, Genes.ENERGY, Genes.DEFENSE]


def create_genome():
    """Creates full genome, used for newborn worm."""
    genotype = []
    genes_for_add = 12
    while genes_for_add > 0:
        genotype.append(random.choice(genes_variations))
        genes_for_add -= 1
    return genotype


def read_names(filename):
    """Creates pool of names from an external file."""
    names = []
    with open(filename, 'r', encoding=None) as reader:
        for line in reader:
            names.append(line.rstrip('\n'))
    return names


worms_names = read_names("names.txt")


class Genetics:
    """The class contains a genotype consisting of genes
    that improve the characteristics of worm instances
    and counters for these bonuses."""

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

    def insertion_mutation(self, inserted_gene: Genes) -> None:
        """Adding gene to the genotype of instance."""
        self.genotype.append(inserted_gene)

    def deletion_mutation(self, deleted_gene: Genes) -> None:
        """Deleting gene from the genotype of instance."""
        self.genotype.remove(deleted_gene)

    def substitution_mutation(self, deleted_gene: Genes, inserted_gene: Genes) -> None:
        """Replaces one random gene with another random one."""
        self.deletion_mutation(deleted_gene)
        self.insertion_mutation(inserted_gene)


class Character:
    """Base class for objects on the map."""

    def __init__(self, coordinates: tuple):
        self.coordinates = coordinates


class Food(Character):
    """Healing objects located on the map."""

    def __init__(self, coordinates: tuple):
        super().__init__(coordinates)
        self.nutritional_value: int = random.randint(1, 5)

    @property
    def eaten(self) -> bool:
        """Return True if the food item has been eaten or lost nutritional_value."""
        return self.nutritional_value <= 0

    def relocation(self, step: tuple, border_x: int, border_y: int) -> None:
        """Relocate food instance on the map."""
        new_coordinates = tuple(map(add, step, self.coordinates))
        new_x = min(max(new_coordinates[0], 0), border_x - 1)
        new_y = min(max(new_coordinates[1], 0), border_y - 1)
        self.coordinates = Cell(new_x, new_y)


class Worm(Character):
    """Main active objects of simulation."""
    def __init__(self, coordinates: tuple):
        super().__init__(coordinates)
        self._name: str = random.choice(worms_names)
        self._health: float = random.randint(6, 9)
        self._damage: float = random.randint(1, 3)
        self._defense: float = random.uniform(0.8, 0.95)
        self._initiative: float = random.randint(1, 3)
        self._energy: float = 100
        self._level: int = 1
        self._experience: int = 0
        self._poisoned: float = 0
        self._divisions_limit: float = 0
        self._generation: float = 0
        self._age: float = 0

        self.genetics = Genetics()

    def get_health(self) -> float:
        """Get _health value of worm instance."""
        return self._health

    def set_health(self, new_health: float) -> None:
        """Set new _health value of worm instance."""
        self._health = new_health

    health = property(get_health, set_health)

    def get_damage(self) -> float:
        """Get _damage value of worm instance."""
        return self._damage

    def set_damage(self, new_damage: float) -> None:
        """Set new _damage value of worm instance."""
        self._damage = new_damage

    damage = property(get_damage, set_damage)

    def get_defense(self) -> float:
        """Get _defense value of worm instance."""
        return self._defense

    def get_initiative(self) -> float:
        """Get _initiative value of worm instance."""
        return self._initiative

    def get_energy(self) -> float:
        """Get _energy value of worm instance."""
        return self._energy

    def set_energy(self, new_energy: float) -> None:
        """Set new _energy value of worm instance."""
        self._energy = new_energy

    energy = property(get_energy, set_energy)

    def get_level(self) -> int:
        """Get _level value of worm instance."""
        return self._level

    def get_poisoned(self) -> float:
        """Get _poisoned value of worm instance."""
        return self._poisoned

    def set_poisoned(self, new_poisoned: float) -> None:
        """Set new _poisoned value of worm instance."""
        self._poisoned = new_poisoned

    poisoned = property(get_poisoned, set_poisoned)

    def get_generation(self) -> float:
        """Get _generation value of worm instance."""
        return self._generation

    def set_generation(self, new_generation: float) -> None:
        """Set new _generation value of worm instance."""
        self._generation = new_generation

    generation = property(get_generation, set_generation)

    def get_divisions_limit(self) -> float:
        """Get _division_limit value of worm instance."""
        return self._divisions_limit

    def set_divisions_limit(self, new_divisions_limit: float) -> None:
        """Set new _division_limit value of worm instance."""
        self._divisions_limit = new_divisions_limit

    divisions_limit = property(get_divisions_limit, set_divisions_limit)

    def get_age(self) -> float:
        """Get _age value of worm instance."""
        return self._age

    def set_age(self, new_age: float) -> None:
        """Set new _age value of worm instance."""
        self._age = new_age

    age = property(get_age, set_age)

    def describe(self) -> None:
        """Displays the main characteristics of worm instance."""
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
        """Every 3 ENERGY gene in the genes pool
        give 1 stat bonus containing in the ENERGY gene."""
        while self.genetics.energetic_genes_pool >= 3:
            self._energy += Genes.ENERGY.value
            self.genetics.energetic_genes_pool -= 3
            self.genetics.energetic_boost += 1
        if self.genetics.energetic_genes_pool < 0:
            self._energy -= Genes.ENERGY.value
            self.genetics.energetic_genes_pool += 3
            self.genetics.energetic_boost -= 1

    def health_genes_realization(self) -> None:
        """Every 4 HEALTH gene in the genes pool
        give 1 stat bonus containing in the HEALTH gene."""
        while self.genetics.health_genes_pool >= 4:
            self._health += Genes.HEALTH.value
            self.genetics.health_genes_pool -= 4
            self.genetics.health_boost += 1
        if self.genetics.health_genes_pool < 0:
            self._health -= Genes.HEALTH.value
            self.genetics.health_genes_pool += 4
            self.genetics.health_boost -= 1

    def damage_genes_realization(self) -> None:
        """Every 5 DAMAGE gene in the genes pool
        give 1 stat bonus containing in the DAMAGE gene."""
        while self.genetics.damage_genes_pool >= 5:
            self._damage += Genes.DAMAGE.value
            self.genetics.damage_genes_pool -= 5
            self.genetics.damage_boost += 1
        if self.genetics.damage_genes_pool < 0:
            self._damage -= Genes.DAMAGE.value
            self.genetics.damage_genes_pool += 5
            self.genetics.damage_boost -= 1

    def defense_genes_realization(self) -> None:
        """Every 5 DEFENSE gene in the genes pool
        give 1 stat bonus containing in the DEFENSE gene."""
        while self.genetics.defense_genes_pool >= 5:
            new_defense_value = self._defense - Genes.DEFENSE.value
            self._defense = max(new_defense_value, 0.2)
            self.genetics.defense_genes_pool -= 5
            self.genetics.defense_boost += 1
        if self.genetics.defense_genes_pool < 0:
            self._defense += Genes.DEFENSE.value
            self.genetics.defense_genes_pool += 5
            self.genetics.defense_boost -= 1

    def newborn_genetics_boost(self, genotype: list) -> None:
        """Fills the pool of each type
         by the number of genes
         of certain types contained in the genotype.
         The method is used when creating a new instance."""
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
        """The method adds a random new gene to the genotype of instance
         and adds 1 to the pool of genes of that type.
         If the pool is full, it increases the characteristic
         corresponding to the type of gene by the value of the gene."""
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
        """Removes a random gene from the genotype of the worm instance,
        reduces the pool of the corresponding type of genes,
        if the pool becomes less than zero,
        then decreases the characteristic of the worm instance
         by the value of the gene."""
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
        """Removes a random gene from the worm's genotype,
        adds a random gene to the genotype,
        checks the corresponding gene pools,
        and implements a bonus / penalty
        on the corresponding pool values."""
        self.deletion_mutation()
        self.insertion_mutation()

    def mutation_metamorphosis(self, mutation: str) -> None:
        """Removes a gene from the genotype of the worm
         and / or adds a gene to the genotype.
         Makes the appropriate changes to the pool of genes to be changed,
         implements the bonus / penalty of the worm characteristics
         corresponding to the pool."""
        if mutation == 'substitution_mutation':
            self.substitution_mutation()
            return
        elif mutation == 'insertion_mutation':
            self.insertion_mutation()
            return
        elif mutation == 'deletion_mutation':
            self.deletion_mutation()

    def level_up(self) -> None:
        """Upgrade level of worm instance, gives a health bonus
        and bonus to one of the three characteristics
        (damage, defense, initiative)."""
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

        self._defense = max(self._defense, 0.2)

        self.division_potential()

    def level_up_damage(self) -> float:
        """Gives bonus of damage and health,
        when level of instance rises."""
        self._damage += 2
        self._health += self._level // 3 + 3
        return self._damage

    def level_up_defense(self) -> float:
        """Gives bonus of defense and health,
        when level of instance rises."""
        self._defense -= self._level / 150 + 0.05
        self._health += self._level // 3 + 3
        return self._defense

    def level_up_initiative(self) -> float:
        """Gives bonus of damage and health,
        when level of instance rises."""
        self._initiative += 1
        self._health += self._level // 3 + 3
        return self._initiative

    def division_potential(self) -> None:
        """Increase division limit by 1."""
        if self._level > 2:
            self._divisions_limit += 1

    @property
    def dead(self) -> bool:
        """Worm is dead, if _health <= 0."""
        return self._health <= 0

    def aging_penalty(self) -> int:
        """Penalty for energy expenditure on movements and strikes,
        increasing with age."""
        if self._age > 100:
            return 3
        elif self._age > 50:
            return 2
        else:
            return 1

    @staticmethod
    def poison(target) -> None:
        """Increasing _poisoned of worm instance for random value."""
        target.poisoned += random.randint(1, 3)

    def poison_effect(self) -> None:
        """With positive poisoning, the worm takes damage,
        the duration of the poisoning decreases."""
        if self.get_poisoned() > 0:
            self._health -= 1
            self.poisoned -= 1

    def is_relative_to(self, other) -> bool:
        """True if the family affinity is below 1e-12.
        Used in the strike method.
        Relatives do not strikes each other,
        do not mix their genotypes
        when creating a child in genetic_variability
        in main module World class."""
        return abs(self.genetics.family_affinity - other.genetics.family_affinity) < 1e-12

    def is_dangerous(self, enemy_health: float) -> bool:
        """An enemy is considered dangerous
        if his life is greater than this worm.
        The method is used to avoid dangerous locations when choosing to move. """
        return enemy_health > self._health

    @staticmethod
    def max_danger_at_location(worms_here: list) -> float:
        """Returns a value equal to the highest value of health in the list of worms. """
        if worms_here:
            return max([worm.get_health() for worm in worms_here])
        else:
            return 0

    def get_safe_steps(self, steps: dict[Enum, list]) -> list:
        """Accepts a dictionary (key = location, value = list of worms in location).
        Returns a list of locations in which the highest health value of the worm
        from the list of worms is less than the health of the current worm. """
        safe_steps = []
        for step in steps:
            if not self.is_dangerous(self.max_danger_at_location(steps.get(step))):
                safe_steps.append(step.value)
        return safe_steps

    @staticmethod
    def get_best_steps(safe_steps: list, steps_with_food: list) -> list:
        """Accepts a list of locations without dangerous enemies
         for this worm and a list of locations with food.
         Returns a list of locations present in both lists."""
        best_steps = []
        for step in steps_with_food:
            if step in safe_steps:
                best_steps.append(step)
        if best_steps:
            return best_steps
        else:
            return safe_steps

    def strike(self, other) -> None:
        """This worm strikes another worm, damaging it
        and has a chance to poison it.
        Energy is consumed per strike with the age penalty.
         This worm gains +1 experience."""
        if not self.dead and self._energy > 0:
            other.health -= self._damage * other.get_defense()
            self._experience += 1
            self._energy -= 2 * self.aging_penalty()
            saving_throw = random.randint(1, 10)
            if saving_throw <= 3:
                self.poison(other)

    def eat(self, target_food) -> None:
        """The worm eats food, gaining a health bonus
         equal to the nutritional value
          and a multiplier energy bonus.
          When a certain energy level is reached,
          the worm's division limit increases."""
        if not self.dead:
            if target_food.nutritional_value > 0:
                self._health += target_food.nutritional_value
                self._energy += target_food.nutritional_value * 5
                target_food.nutritional_value = 0
                if self._energy > 150:
                    self._divisions_limit += 1
                    self._energy -= 50

    def move(self, step: tuple, border_x: int, border_y: int) -> None:
        """The worm moves to another cell wasting energy with aging penalty."""
        if not self.dead and self._energy > 0:
            self._energy -= 1 * self.aging_penalty()
            new_coordinates = tuple(map(add, step, self.coordinates))
            new_x = min(max(new_coordinates[0], 0), border_x - 1)
            new_y = min(max(new_coordinates[1], 0), border_y - 1)
            self.coordinates = Cell(new_x, new_y)
