from Entities.Player import Player
from Actions.Card import Card


class EmptyMind(Card):
    def __init__(self):
        super().__init__("EmptyMind", 1, 0, 0, 0, 0, 0, False, "", Player.Stance.NONE)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Exit your {{Stance}}. Draw 2(3) cards.
