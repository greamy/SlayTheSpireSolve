from Entities.Player import Player
from Actions.Card import Card


class Sanctity(Card):
    def __init__(self):
        super().__init__("Sanctity", 1, 0, 0, 6, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 6(9) {{Block}}. If the previous card played was a Skill, draw 2 card.
