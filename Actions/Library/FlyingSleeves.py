from Entities.Player import Player
from Actions.Card import Card


class FlyingSleeves(Card):
    def __init__(self):
        super().__init__("FlyingSleeves", 1, 4, 1, 0, 0, 0, False, "", None)