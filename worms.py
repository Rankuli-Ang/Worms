import random

# Worms naming
names_txt = 'Names.txt'
number_of_battles_txt = 'Number_of_Battles.txt'
worms_names_list = []


def worms_naming():
    global worms_names_list
    with open(names_txt) as raw_worms_names_file:
        lines = list(raw_worms_names_file)
        for line in lines:
            line.rstrip('\n')
            worms_names_list.append(line)
    return worms_names_list


worms_naming()


# Worms constructor

class Worm:
    def __init__(self):
        self.name: str = random.choice(worms_names_list)
        self.health: int = random.randint(6, 12)
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.5, 1.0)
        self.initiative: int = random.randint(1, 10)
        self.experience: int = 0
        self.level: int = 1
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
        if self.experience >= self.level + 3:
            self.level += 1
            self.experience = 0
            level_ups.get('damage' or 'defense' or 'initiative')

    def level_up_damage(self):
        self.damage += self.level + 2
        self.health += self.level // 3 + 3

    def level_up_defense(self):
        self.defense -= self.level / 200 + 0.05
        if self.defense < 0.2:
            self.defense = 0.2
        self.health += self.level // 3 + 3

    def level_up_initiative(self):
        self.initiative += 1
        self.health += self.level // 3 + 3

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def poison_effect(self):
        if self.poisoned > 0:
            self.health -= 1
            self.poisoned -= 1

    def strike(self, other):
        other.health -= self.damage * other.defense
        return other.health

    def death(self):
        self.already_dead += 1
        return self.already_dead


class Defiler(Worm):
    def __init__(self):
        super(Defiler, self).__init__()
        self.already_dead: int = 0

    def death(self):
        self.already_dead += 1
        amount = 0
        while amount < 3:
            worms_list.append(Zerling())
            amount += 1
        return self.already_dead


class Zerling(Worm):
    def __init__(self):
        super(Zerling, self).__init__()
        self.health: int = random.randint(3, 5)
        self.damage: int = random.randint(1, 2)
        self.defense: float = random.uniform(0.8, 1.0)
        self.initiative: int = random.randint(5, 10)
        self.experience: int = 2
        self.level: int = 1
        self.poisoned: int = 0
        self.already_dead: int = 0


class Infectoid(Worm):
    def __init__(self):
        super(Infectoid, self).__init__()

    def strike(self, other):
        other.health = other.health - self.damage
        other.poisoned += 3
        return other.health


# Other globals

def corpsegrinding():
    all_remains = 0
    remains = 0
    for dead in worms_list:
        if dead.already_dead != 0:
            worms_list.remove(dead)
            all_remains += 3
    if len(worms_list) > 0:
        remains = all_remains / len(worms_list)
    for eater in worms_list:
        eater.health += remains


class Statistics:
    def __init__(self):
        self.number_of_battles: int = 0

    def count(self):
        self.number_of_battles += 1


level_ups = {'damage': Worm.level_up_damage, 'defense': Worm.level_up_defense, 'initiative': Worm.level_up_initiative}

worms_list = []
