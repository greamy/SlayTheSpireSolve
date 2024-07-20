from Entities.Player import Player
from Actions.Card import Card


class FlurryofBlows(Card):
    def __init__(self):
        super().__init__("FlurryofBlows", 0, 4, 1, 0, 0, 0, False, "", None)