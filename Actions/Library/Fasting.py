from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Fasting(Card):
    def __init__(self):
        super().__init__("Fasting", Card.Type.POWER, 2, 0, 0, 0, 0, 0, False, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Strength}}. Gain 3(4) {{Dexterity}}. Gain 1 less {{Energy}} at the start of each turn.
