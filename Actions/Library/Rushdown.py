from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Rushdown(Card):
    def __init__(self):
        super().__init__("Rushdown", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Whenever you enter {{Wrath}}, draw 2 cards.
