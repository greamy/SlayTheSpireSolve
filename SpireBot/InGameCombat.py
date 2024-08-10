import json
import time

from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from SpireBot.Environments.SpireEnvironment import SpireEnvironment
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


class InGameCombat:

    def __init__(self, environment, player_state, enemies: list[Enemy], logger: Logger, bot: SpireBot, debug: bool):
        self.player_state = player_state
        self.bot = bot
        self.environment = environment

        if len(enemies) < 1:
            print("No enemies in combat")

        self.enemies = enemies

        self.logger = logger
        self.debug = debug

    def start(self):
        # self.player.begin_combat()
        return self.run()

    def get_total_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def run(self):
        # First, get state
        # Game loop of player turn:
        #   get possible actions
        #   ask bot to choose action
        #   get new state
        # repeat until no playable cards
        # until 'end turn', then get new state and repeat..

        try:
            decoder = json.JSONDecoder()
            state = self.environment.get_state()
            while "play" in state['available_commands']:
                time.sleep(1)
                state = self.environment.get_state()
            self.logger.close()
        except Exception as e:
            self.logger.write(str(e))
            self.logger.err_write(str(e))
        finally:
            self.logger.close()






