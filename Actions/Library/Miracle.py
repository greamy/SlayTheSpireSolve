
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Miracle(Card):
    def __init__(self, player: Player):
        super().__init__("Miracle", Card.Type.SKILL, -1, 0, 0, 0, 0, 0, True, True, player, None)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Retain. Gain 1(2) energy. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = -2
