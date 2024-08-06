from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Nirvana(Card):
    def __init__(self, player: Player):
        super().__init__("Nirvana", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.scry_block = 3
        self.listener = Listener(Listener.Event.SCRY_OCCURRED, self.do_power)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Whenever you {{Scry}}, gain 3(4) {{Block}}.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        player.block += self.scry_block

    def upgrade(self):
        super().upgrade()
        self.scry_block = 4
