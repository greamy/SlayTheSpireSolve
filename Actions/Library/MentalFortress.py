from Entities.Player import Player
from Actions.Card import Card


class MentalFortress(Card):
    def __init__(self):
        super().__init__("MentalFortress", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Whenever you switch {{Stance|Stances}}, gain 4(6) {{Block}}.
