from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Collect(Card):
    def __init__(self):
        super().__init__("Collect", 0, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.
