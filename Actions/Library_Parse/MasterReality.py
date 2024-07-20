from Entities.Player import Player
from Actions.Card import Card


class MasterReality(Card):
    def __init__(self):
        super().__init__("MasterReality", 1, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Whenever a card is created during combat, {{Upgrade}} it.
