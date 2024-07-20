from Entities.Player import Player
from Actions.Card import Card


class LessonLearned(Card):
    def __init__(self):
        super().__init__("LessonLearned", 2, 10, 1, 0, 0, 0, True, "", None)