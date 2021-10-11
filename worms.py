"""The module in which the visualization takes place,
the implementation of the mechanics
of worms, food, weather events."""
import configparser
import logging


import src.processors
import src.world

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    logging_levels = {'DEBUG': logging.DEBUG,
                      'INFO': logging.INFO,
                      'WARNING': logging.WARNING,
                      'ERROR': logging.ERROR,
                      'CRITICAL': logging.CRITICAL}

    logging_level = config.get('LOGGER', 'level')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging_levels.get(logging_level))

    WORLD_HEIGHT = int(config.get('WORLD', 'height'))
    WORLD_WIDTH = int(config.get('WORLD', 'width'))
    WORLD_START_WORMS_NUM = int(config.get('WORLD', 'worms_num'))
    WORLD_START_FOOD_NUM = int(config.get('WORLD', 'food_num'))

    world = src.world.World(WORLD_HEIGHT, WORLD_WIDTH, WORLD_START_WORMS_NUM, WORLD_START_FOOD_NUM)
    valid_processors = {
        'agingprocessor': src.processors.AgingProcessor,
        'zeroenergyprocessor': src.processors.ZeroEnergyProcessor,
        'poisonprocessor': src.processors.PoisonProcessor,
        'weathereventsemergenceprocessor': src.processors.WeatherEventsEmergenceProcessor,
        'addfoodprocessor': src.processors.AddFoodProcessor,
        'weathermovementsprocessor': src.processors.WeatherMovementsProcessor,
        'weathereffectsprocessor': src.processors.WeatherEffectsProcessor,
        'wormsmovementprocessor': src.processors.WormsMovementProcessor,
        'fightprocessor': src.processors.FightProcessor,
        'corpsegrindingprocessor': src.processors.CorpseGrindingProcessor,
        'foodpickupprocessor': src.processors.FoodPickUpProcessor,
        'deadwormsremover': src.processors.DeadWormsRemover,
        'eatenfoodremover': src.processors.EatenFoodRemover,
        'weathereventsremover': src.processors.WeatherEventsRemover,
        'levelupprocessor': src.processors.LevelUpProcessor,
        'wormdivisionprocessor': src.processors.WormDivisionProcessor,
        'mutationprocessor': src.processors.MutationProcessor,
        'analyticsprocessor': src.processors.AnalyticsProcessor,
        'visualizer': src.processors.Visualizer}

    processors = []

    for option in config.options('PROCESSORS'):
        if option not in valid_processors.keys():
            logging.error('Unknown processor')
            raise ValueError('Unknown processor')
        if config.getboolean('PROCESSORS', option) is True:
            proc = valid_processors[option]
            processors.append(proc())

    PROCESS = True

    while PROCESS is True:
        for proc in processors:
            proc.process(world)
