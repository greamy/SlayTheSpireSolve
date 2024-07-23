from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class CutThroughFate(Card):
    def __init__(self):
        super().__init__("CutThroughFate", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.
