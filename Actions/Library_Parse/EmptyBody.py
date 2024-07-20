from Entities.Player import Player
from Actions.Card import Card


class EmptyBody(Card):
    def __init__(self):
        super().__init__("EmptyBody", 1, 0, 0, 7, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Gain 7(10) {{Block}}. Exit your {{Stance}}.
