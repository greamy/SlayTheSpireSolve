from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
import random

class LessonLearned(Card):
    def __init__(self, player: Player):
        super().__init__("LessonLearned", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, True, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 10(13) damage. If {{Fatal}}, {{Upgrade}} a random card in your deck. {{Exhaust}}.
        if not target_enemy.minion and not target_enemy.is_alive():
            random.choice(player.deck.get_deck()).upgrade()

    def upgrade(self):
        super().upgrade()
        self.damage = 13
