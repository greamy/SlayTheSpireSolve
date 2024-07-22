from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class SandsofTime(Card):
    def __init__(self):
        super().__init__("SandsofTime", Card.Type.ATTACK, 4, 20, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 20(26) damage. Whenever this card is {{Retain|Retained}}, lower its cost by 1.
