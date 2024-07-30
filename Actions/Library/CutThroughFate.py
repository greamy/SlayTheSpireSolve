from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class CutThroughFate(Card):
    def __init__(self):
        super().__init__("CutThroughFate", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, "", None)
        self.scry_amount = 2
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.
        player.scry(self.scry_amount)
        player.draw_cards(1)

    def upgrade(self):
        super().upgrade()
        self.damage = 9
        self.scry_amount = 3
