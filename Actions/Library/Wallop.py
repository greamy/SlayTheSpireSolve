from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Wallop(Card):
    def __init__(self):
        super().__init__("Wallop", Card.Type.ATTACK, 2, 9, 1, , 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 9(12) damage. Gain {{Block}} equal to unblocked damage dealt.
