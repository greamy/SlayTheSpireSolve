from Entities.Player import Player
from Actions.Card import Card


class DeceiveReality(Card):
    def __init__(self):
        super().__init__("DeceiveReality", 1, 0, 0, 4, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.
