from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Devotion(Card):
    def __init__(self, player: Player):
        super().__init__("Devotion", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.mantra = 2
        self.listener = Listener(Listener.Event.START_TURN, self.do_power)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_listener(self.listener)
        # At the start of your turn, gain 2(3) {{Mantra}}.

    def do_power(self, player, enemy, enemies, debug):
        player.add_mantra(self.mantra)

    def upgrade(self):
        super().upgrade()
        self.mantra = 3


