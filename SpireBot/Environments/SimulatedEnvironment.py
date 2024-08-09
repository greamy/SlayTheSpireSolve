from Combat import Combat
from SpireBot.Environments.Environment import Environment


class SimulatedEnvironment(Environment):
    def __init__(self, player, enemies, debug):
        super().__init__()
        self.player = player
        self.enemies = enemies
        self.debug = debug
        combat = Combat(player, enemies, debug)

    def get_state(self) -> dict:
        pass