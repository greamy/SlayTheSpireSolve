from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class LessonLearned(Card):
    def __init__(self):
        super().__init__("LessonLearned", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, True, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 10(13) damage. If {{Fatal}}, {{Upgrade}} a random card in your deck. {{Exhaust}}.
