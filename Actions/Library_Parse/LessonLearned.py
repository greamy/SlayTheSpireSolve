from Entities.Player import Player
from Actions.Card import Card


class LessonLearned(Card):
    def __init__(self):
        super().__init__("LessonLearned", 2, 10, 1, 0, 0, 0, True, "", None)
        
    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # Deal 10(13) damage. If {{Fatal}}, {{Upgrade}} a random card in your deck. {{Exhaust}}.
