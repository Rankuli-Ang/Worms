import random

names_txt = 'Names.txt'
worms_names_list = []


class Worm:
    def __init__(self):
        self.name: str = random.choice(worms_names_list)
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
        if self.experience >= self.level + 2:
            self.level += 1
            self.experience = 0
            level_ups = [self.level_up_damage(), self.level_up_initiative(), self.level_up_defense()]
            level_ups_without_def = [self.level_up_damage(), self.level_up_initiative()]
            if self.defense <= 0.2:
                self.defense = 0.2
                level_ups_value = random.choice(level_ups_without_def)
                if level_ups_value == level_ups_without_def[0]:
                    self.level_up_damage()
                else:
                    self.level_up_initiative()
            else:
                level_ups_value = random.choice(level_ups)
                if level_ups_value == level_ups[0]:
                    self.level_up_damage()
                elif level_ups_value == level_ups[1]:
                    self.level_up_initiative()
                else:
                    self.level_up_defense()

    def level_up_damage(self):
        self.damage += 2
        self.health += self.level // 3 + 3

    def level_up_defense(self):
        self.defense -= self.level / 150 + 0.05
        self.health += self.level // 3 + 3

    def level_up_initiative(self):
        self.initiative += 1
        self.health += self.level // 3 + 3

    def alive_check(self):
        if self.health <= 0:
            self.already_dead += 1
            return self.already_dead

    def strike(self, other):
        other.health -= self.damage * other.defense
        return other.health

    def poison_effect(self):
        if self.poisoned > 0:
            self.health -= 1
            self.poisoned -= 1


def worms_naming():
    global worms_names_list
    with open(names_txt) as raw_worms_names_file:
        lines = list(raw_worms_names_file)
        for line in lines:
            line.rstrip('\n')
            worms_names_list.append(line)
    return worms_names_list


'''
def corpsegrinding():
    global worms_list
    remains = 0
    alive_worms = []
    for alive in worms_list:
        if alive.is_alive() is True:
            alive_worms.append(alive)

    corpses = (len(worms_list) - len(alive_worms))
    worms_list.clear()
    for un in alive_worms:
        worms_list.append(un)
    if corpses > 0:
        remains = corpses * 3 / len(worms_list)
    for eater in worms_list:
        eater.health += remains
    alive_worms.clear()
    return worms_list
'''
