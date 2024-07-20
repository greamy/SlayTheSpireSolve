from Entities.Player import Player
from Actions.Card import Card


class Vault(Card):
    def __init__(self):
        super().__init__("Vault", 3, 0, 0, 0, 0, 0, True, "", None)