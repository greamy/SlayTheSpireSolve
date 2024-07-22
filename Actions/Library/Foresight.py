from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Foresight(Card):
    def __init__(self):
        super().__init__("Foresight", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the start of your turn, {{Scry}} 3(4).
