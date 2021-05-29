import random

# Переменные (я так понимаю что выносить их таким образом не совсем корректно)
Name = 0
Health = 0
Damage = 0
Defense = 0
Initiative = 0
Experience = 0
Level = 0
Corpses = 0
Remains = 0
Rounds = 0
number_of_battles = 0
level_up_variations = ['damage', 'defense', 'initiative']
level_up_value = 0
Scourge = 0

# Формирование списка имён червей
Worms_names_list = ["asd"]
# Корпус червей


a = {}
a = {"id": "a"}
print(a)
class Worm:
    def __init__(self):
        self.name: Name = random.choice(Worms_names_list)
        self.health: Health = random.randint(6, 12)
        self.damage: Damage = random.randint(1, 3)
        self.defense: Defense = random.uniform(0.5, 1.0)
        self.initiative: Initiative = random.randint(1, 10)
        self.experience: Experience = 0
        self.level: Level = 1

    def describe(self) -> None:
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
    def regeneration(self):
        pass

    def strike(self, other):
        other.health = other.health - self.damage * other.defense
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

            self.strike (other)
            self.experience += 1
            self.level_up()
            other.death()


class Hydralisk(Worm):
    def __init__(self):
        super(Hydralisk, self).__init__()

    def regeneration(self):
        self.health += 2
        return self.health

    def death(self):
        self.regeneration()
        super(Hydralisk, self).death()


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
    worms = [Worm() for i in range(1, 51)] + [Hydralisk()]

    while len(worms) > 1:
        warrior1 = random.choice(worms)
        warrior2 = random.choice(worms)
        if warrior1 != warrior2:
            warrior1.attack(warrior2)


    print('Number of battles:')
    print(number_of_battles)


    print('Total Number of battles:')

    if len(worms) == 1:
        print(worms[0].describe())
        worms.append(Hydralisk())
        worms[1].describe()
    else:
        print('All is dead!')



