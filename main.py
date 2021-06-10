import random
import worms

if __name__ == "__main__":

    defilers_list = [worms.Defiler() for i in range(1, 11)]
    zerlings_list = [worms.Zerling() for i in range(1, 21)]
    infectoids_list = [worms.Infectoid() for i in range(1, 6)]
    worms_list = defilers_list + zerlings_list + infectoids_list

    Counter = worms.Statistics()

    while len(worms_list) > 1:
        worms.corpsegrinding()
        if len(worms_list) <= 1:
            break
        worms_list.sort(key=lambda worm: worm.initiative)
        for unit in worms_list:
            if unit.already_dead != 0:
                continue
            unit.poison_effect()
            if unit.is_alive() is False:
                unit.death()
                continue
            enemy = random.choice(worms_list)

            if unit == enemy:
                pass
            else:
                Counter.count()
                if unit.initiative >= enemy.initiative:
                    unit.strike(enemy)
                    unit.experience += 1
                    unit.level_up()
                    if enemy.is_alive() is False:
                        enemy.death()
                        continue

                    enemy.strike(unit)
                    enemy.experience += 1
                    enemy.level_up()
                    if unit.is_alive() is False:
                        unit.death()
                        continue

                else:
                    enemy.strike(unit)
                    enemy.experience += 1
                    enemy.level_up()
                    if unit.is_alive() is False:
                        unit.death()
                        continue

                    unit.strike(enemy)
                    unit.experience += 1
                    unit.level_up()
                    if enemy.is_alive() is False:
                        enemy.death()
                        continue

    print('Number of battles:', Counter.number_of_battles)

    with open(worms.number_of_battles_txt) as nobf:
        number_of_battles_file = nobf.read()
        number_of_battles_total = int(number_of_battles_file) + Counter.number_of_battles
        nobf.close()

    print('Total Number of battles:', number_of_battles_total)

    with open(worms.number_of_battles_txt, 'w') as nobf:
        nobf.write(str(number_of_battles_total))

    if len(worms_list) == 1:
        print(worms_list[0].describe())
        print(type(worms_list[0]))
    else:
        print('All is dead!')
