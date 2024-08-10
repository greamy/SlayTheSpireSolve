import json
import time

from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player

from SpireBot.Environments.Environment import Environment
from SpireBot.Environments.States.Map import Map


class SpireEnvironment(Environment):

    def __init__(self):
        super().__init__()
        self.decoder = json.JSONDecoder()
        self.state: dict = self.get_state()

    def get_state(self) -> (Player, list[Enemy], Map):
        raw_state = input()
        self.state = self.decoder.decode(raw_state)

    def request_state(self):
        print("STATE")
        self.state = input()
        return self.state

    def get_possible_actions(self) -> list:
        commands = self.state['available_commands']
        game_state = self.state['game_state']

        actions = commands
        # if game_state['screen_type'] == "EVENT" and "choose" in commands:
        #     for choice in game_state['choice_list']:
        #         actions.append("choose " + choice)
        if "play" in commands:
            pass
        return actions
