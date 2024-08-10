import json
import time

from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


class InGameCombat:

    def __init__(self, player_state, enemies: list[Enemy], logger: Logger, bot: SpireBot, debug: bool):
        self.player_state = player_state
        self.bot = bot

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
        pass

        try:
            decoder = json.JSONDecoder()
            # print("READY")
            # self.state = input()
            # print("START Watcher 0")
            while self.state['']:
                time.sleep(1)
                self.state = input()
                self.logger.write(self.state)
                self.state = decoder.decode(self.state)
                self.process_state(self.state)
            self.logger.close()
        except Exception as e:
            self.logger.write(str(e))
            self.logger.err_write(str(e))

    def process_state(self, state):
        try:
            game_ready = state['ready_for_command']
            if not game_ready:
                self.logger.write("Game not ready for commands.")
                return
            commands = state['available_commands']
            if "choose" in commands:
                self.choose_option_random(state)
        except KeyError:
            self.logger.write("State has no available commands.")

    def choose_option_random(self, state):
        try:
            choices = state['game_state']['choice_list']
            self.logger.write(str(choices))
        except KeyError:
            self.logger.write("ERROR: No Choices Available. Might be in combat.")
            return
        choice = random.choice(choices)
        self.logger.write("Chosen " + str(choice) + " from " + str(choices))
        print("CHOOSE " + str(choice))




