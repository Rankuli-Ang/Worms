import random

corpses = 0
remains = 0
number_of_battles = 0
level_up_variations = ['damage', 'defense', 'initiative']
names_txt = 'Names.txt'
number_of_battles_txt = 'Number_of_Battles.txt'


# Корпус червей

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
        self.damage += self.level + 2
        self.health = self.health + self.level / 3 + 3

    def level_up_defense(self):
        self.defense -= self.level / 200 + 0.05
        if self.defense < 0.2:
            self.defense = 0.2
        self.health = self.health + self.level / 3 + 3

    def level_up_initiative(self):
        self.initiative += 1
        self.health = self.health + self.level / 3 + 3

    def death(self):
        if self.health <= 0:
            global corpses
            corpses += 1
            return worms.remove(self)

    def strike(self, other):
        other.health = other.health - self.damage * other.defense
        return other.health

    def attack(self, other):
        global number_of_battles
        number_of_battles = number_of_battles + 1
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
            global corpses
            corpses += 1
            amount = 0
            while amount < 4:
                worms.append(Zerling())
                amount += 1
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

    def strike(self, other):
        other.health = other.health - self.damage
        other.poisoned += 3
        return other.health

    def death(self):
        if self.health <= 0:
            global corpses
            corpses += 1
            return worms.remove(self)


def corpsegrinding():
    global remains
    remains = corpses / len(worms)

    def feeding():
        nonlocal eater
        eater.health = eater.health + remains * 0.5
        return eater.health

    for eater in worms:
        feeding()
    remains = 0


# Тело программы
if __name__ == "__main__":

    # Формирование списка имён червей
    worms_names_list = []
    with open(names_txt) as raw_worms_names_file:
        lines = list(raw_worms_names_file)
        for line in lines:
            line.rstrip('\n')
            worms_names_list.append(line)

    defilers_list = [Defiler() for i in range(1, 11)]
    zerlings_list = [Zerling() for i in range(1, 21)]
    infectoids_list = [Infectoid() for i in range(1, 6)]
    worms = defilers_list + zerlings_list + infectoids_list

    while len(worms) > 1:
        worms.sort(key=lambda worm: worm.initiative)
        for unit in worms:
            if unit.poisoned > 0:
                unit.health -= 1
                unit.poisoned -= 1
                unit.death()
                continue
            enemy = random.choice(worms)
            if unit == enemy:
                pass
            else:
                unit.attack(enemy)
        corpsegrinding()

    print('Number of battles:', number_of_battles)

    with open(number_of_battles_txt) as nobf:
        number_of_battles_file = nobf.read()
        number_of_battles_total = int(number_of_battles_file) + number_of_battles
        nobf.close()

    print('Total Number of battles:', number_of_battles_total)

    with open(number_of_battles_txt, 'w') as nobf:
        nobf.write(str(number_of_battles_total))

    if len(worms) == 1:
        print(worms[0].describe())
        print(type(worms[0]))
    else:
        print('All is dead!')
