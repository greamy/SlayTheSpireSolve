from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class FlyingSleeves(Card):
    def __init__(self):
        super().__init__("FlyingSleeves", Card.Type.ATTACK, 1, 4, 1, 0, 0, 0, False, True, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 4(6) damage twice.
