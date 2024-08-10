from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from SpireBot.Environments.States.Map import Map


class Environment:

    def __init__(self):
        self.state = None

    def get_state(self) -> (Player, list[Enemy], Map):
        pass
