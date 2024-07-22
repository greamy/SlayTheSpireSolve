from Entities.Player import Player
from Actions.Card import Card


class Halt(Card):
    def __init__(self):
        super().__init__("Halt", 0, 0, 0, 3, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Block}}. {{Wrath}}: Gain 9(14) additional {{Block}}.
