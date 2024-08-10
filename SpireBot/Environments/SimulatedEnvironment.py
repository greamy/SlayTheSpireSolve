from Combat import Combat
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from SpireBot.Environments.Environment import Environment
from SpireBot.Environments.States.Map import Map


class SimulatedEnvironment(Environment):
    def __init__(self, player: Player, enemies: list[Enemy], debug: bool, act=1, ascension=20):
        super().__init__()
        self.player = player
        self.enemies = enemies
        self.map = Map.generate_map(act, ascension)
        self.debug = debug
        combat = Combat(player, enemies, debug)

    def get_state(self) -> (Player, list[Enemy], Map):
        return self.player, self.enemies, self.map

    def get_actions(self) -> list:
        pass
 