from Entities.Player import Player
from Actions.Card import Card


class Wish(Card):
    def __init__(self):
        super().__init__("Wish", 3, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Choose one: Gain 6(8) {{Plated Armor}}, 3(4) {{Strength}}, or 25(30) Gold. {{Exhaust}}.
