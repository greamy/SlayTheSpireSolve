from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class LessonLearned(Card):
    def __init__(self, player: Player):
        super().__init__("LessonLearned", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, True, False, player, None)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 10(13) damage. If {{Fatal}}, {{Upgrade}} a random card in your deck. {{Exhaust}}.
        if not target_enemy.minion and not target_enemy.is_alive():
            random.choice(player.deck.get_deck([self])).upgrade()

    def upgrade(self):
        super().upgrade()
        self.damage = 13
