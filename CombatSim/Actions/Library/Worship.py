from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Worship(Card):
    def __init__(self, player: Player):
        super().__init__("Worship", Card.Type.SKILL, 2, 0, 0, 0, 0, 0, False, False, player, None)
        self.mantra = 5
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # ({{Retain}}.) Gain 5 {{Mantra}}.
        super().play(player, target_enemy, enemies, debug)
        player.add_mantra(self.mantra)


    def upgrade(self):
        self.retain = True
