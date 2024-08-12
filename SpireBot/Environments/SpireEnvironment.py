import json
import time

from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player

from SpireBot.Environments.Environment import Environment
from SpireBot.Environments.States.Map import Map
from SpireBot.InGameCombat import InGameCombat
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


class SpireEnvironment(Environment):

    def __init__(self, logger: Logger):
        super().__init__()
        self.decoder = json.JSONDecoder()
        self.state: dict = None
        self.bot = SpireBot()
        self.logger = logger

    def run(self):
        print("READY")
        self.get_state()
        print("START Watcher 0")
        # Click through menus
        while True:
            time.sleep(1)
            self.get_state()
            self.process_state(self.state)

    def process_state(self, state: dict):
        try:
            game_ready = state['ready_for_command']
            if not game_ready:
                self.logger.write("Game not ready for commands.")
                return
            commands = state['available_commands']
            if "choose" in commands:
                possible_choices = self.get_possible_actions()
                choice = self.bot.choose_option(self.get_possible_actions(), None)
                self.logger.write("Chose " + str(choice) + " from " + str(possible_choices))
                print(choice)
            elif "play" in commands:
                combat = InGameCombat(self.state, self, None, self.logger, self.bot, False)
                combat.start()
        except KeyError:
            self.logger.write("State has no available commands.")

    def get_state(self):
        raw_state = input()
        self.logger.write("raw: " + str(raw_state))
        self.state = self.decoder.decode(raw_state)
        self.logger.write(self.state)
        return self.state

    def request_state(self):
        print("STATE")
        self.state = input()
        return self.state

    def get_possible_actions(self) -> list:
        commands = self.state['available_commands']
        game_state = self.state['game_state']

        actions = []
        if (game_state['screen_type'] == "EVENT" or game_state['screen_type'] == "MAP") and "choose" in commands:
            for choice in game_state['choice_list']:
                actions.append("choose " + choice)
        if "play" in commands:
            cards_in_hand = game_state['combat_state']['hand']
            self.logger.write("Available cards: " + str(cards_in_hand))
            actions = cards_in_hand
        return actions

    def get_menu_options(self, state):
        try:
            choices = state['game_state']['choice_list']
            self.logger.write(str(choices))
        except KeyError:
            self.logger.write("ERROR: No Choices Available. Might be in combat.")
            return
