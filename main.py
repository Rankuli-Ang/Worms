import random

Corpses = 0
Remains = 0
Rounds = 0
number_of_battles = 0
level_up_variations = ['damage', 'defense', 'initiative']

# Формирование списка имён червей
Worms_names_list = []
Raw_worms_names_file = open('Names.txt')
lines = list(Raw_worms_names_file)
for line in lines:
    Nms = line[:-1]
    Worms_names_list.append(Nms)


# Корпус червей

class Worm:
    def __init__(self):
        self.name: str = random.choice(Worms_names_list)
        self.health: int = random.randint(6, 12)
        self.damage: int = random.randint(1, 3)
        self.defense: float = random.uniform(0.5, 1.0)
        self.initiative: int = random.randint(1, 10)
        self.experience: int = 0
        self.level: int = 1
        self.poisoned: int = 0

    def describe(self):
        print(f'Worm {self.name}:')
        print(f'\thealth {self.health}')
        print(f'\tdamage {self.damage}')
        print(f'\tdefense {self.defense}')
        print(f'\tinitiative {self.initiative}')
        print(f'\tlevel {self.level}')
        print(f'\texperience {self.experience}')

    def level_up(self):
        if self.experience >= self.level + 3:
            self.level += 1
            self.experience = 0
            level_up_value = random.choice(level_up_variations)
            if level_up_value == level_up_variations[0]:
                self.level_up_damage()
            elif level_up_value == level_up_variations[1]:
                self.level_up_defense()
            else:
                self.level_up_initiative()

    def level_up_damage(self):
        self.damage = self.level + 2
        self.health = self.level + 5

    def level_up_defense(self):
        self.defense -= self.level / 200 + 0.05
        if self.defense < 0.2:
            self.defense = 0.2
        self.health = self.level + 5

    def level_up_initiative(self):
        self.initiative = self.level + 1
        self.health = self.level + 5

    def death(self):
        if self.health <= 0:
            global Corpses
            Corpses += 1
            return worms.remove(self)

    def poisoning(self, other):
        pass

    def strike(self, other):
        other.health = other.health - self.damage * other.defense
        self.poisoning(other)
        return other.health

    def attack(self, other):
        global number_of_battles
        number_of_battles = number_of_battles + 1
        global Rounds
        Rounds += 1
        if Rounds >= 10:
            if Corpses >= 1:
                corpsegrinding()
        if self.initiative >= other.initiative:

            self.strike(other)
            self.experience += 1
            self.level_up()
            other.death()

            other.strike(self)
            other.experience += 1
            other.level_up()
            self.death()

        else:

            other.strike(self)
            other.experience += 1
            other.level_up()
            self.death()

            self.strike(other)
            self.experience += 1
            self.level_up()
            other.death()


class Defiler(Worm):
    def __init__(self):
        super(Defiler, self).__init__()

    def death(self):
        if self.health <= 0:
            global Corpses
            Corpses += 1
            worms.append(Zerling())
            worms.append(Zerling())
            worms.append(Zerling())
            worms.append(Zerling())
            worms.append(Zerling())
            return worms.remove(self)


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


class Infectoid(Worm):
    def __init__(self):
        super(Infectoid, self).__init__()

    def poisoning(self, other):
        other.poisoned += 3
        return other.poisoned

    def strike(self, other):
        other.health = other.health - self.damage
        self.poisoning(other)
        return other.health

    def death(self):
        if self.health <= 0:
            global Corpses
            Corpses += 1
            worms.remove(random.choice(worms))
            return worms.remove(self)


def corpsegrinding():
    global Remains
    global Rounds
    Remains = Corpses / len(worms)

    def feeding():
        nonlocal eater
        eater.health = eater.health + Remains
        return eater.health

    for eater in worms:
        feeding()
    Remains = 0
    Rounds = 0


# Тело программы
if __name__ == "__main__":
    Defilers_list = [Defiler() for i in range(1, 11)]
    Zerlings_list = [Zerling() for i in range(1, 21)]
    Infectoids_list = [Infectoid() for i in range(1, 6)]
    worms = Defilers_list + Zerlings_list + Infectoids_list

    while len(worms) > 1:
        for unit in worms:
            if unit.poisoned > 0:
                unit.health -= 1
                unit.death()
        warrior1 = random.choice(worms)
        warrior2 = random.choice(worms)
        if warrior1 != warrior2:
            warrior1.attack(warrior2)

    print('Number of battles:')
    print(number_of_battles)

    Number_of_Battles_file = open('Number_of_Battles.txt').read()
    Number_of_Battles_raw = int(Number_of_Battles_file) + number_of_battles

    print('Total Number of battles:')
    print(Number_of_Battles_raw)

    Number_of_Battles_file = open('Number_of_Battles.txt', 'w')
    Number_of_Battles_file.write(str(Number_of_Battles_raw))
    Number_of_Battles_file.close()

    if len(worms) == 1:
        print(worms[0].describe())
        print(type(worms[0]))
    else:
        print('All is dead!')
