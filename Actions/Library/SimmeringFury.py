from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class SimmeringFury(Card):
    def __init__(self):
        super().__init__("SimmeringFury", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the start of your next turn, enter {{Wrath}} and draw 2(3) cards.
