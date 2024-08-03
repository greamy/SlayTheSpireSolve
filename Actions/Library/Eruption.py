from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Eruption(Card):
    def __init__(self, player: Player):
        super().__init__("Eruption", Card.Type.ATTACK, 2, 9, 1, 0, 0, 0, False, False, player, Player.Stance.WRATH)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 9 damage. Enter {{Wrath}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 1
