from Entities.Player import Player
from Actions.Card import Card


class CrushJoints(Card):
    def __init__(self):
        super().__init__("CrushJoints", 1, 8, 1, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.
