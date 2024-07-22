from Entities.Player import Player
from Actions.Card import Card


class Indignation(Card):
    def __init__(self):
        super().__init__("Indignation", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.
