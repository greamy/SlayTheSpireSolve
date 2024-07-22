from Entities.Player import Player
from Actions.Card import Card


class DeusExMachina(Card):
    def __init__(self):
        super().__init__("DeusExMachina", 1000, 0, 0, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # {{Unplayable}}. When you draw this card, add 2(3) {{C|Miracle|Miracles}} into your hand. {{Exhaust}}.
