from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class WindmillStrike(Card):
    def __init__(self):
        super().__init__("WindmillStrike", Card.Type.ATTACK, 2, 7, 1, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 7(10) damage. Whenever this card is {{Retain|Retained}}, increase its damage by 4(5).
