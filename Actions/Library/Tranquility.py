from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Tranquility(Card):
    def __init__(self, player: Player):
        super().__init__("Tranquility", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, True, player, Player.Stance.CALM)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Enter {{Calm}}. {{Exhaust}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 0
