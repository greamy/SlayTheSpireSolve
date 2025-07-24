from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
import random


class LessonLearned(Card):
    def __init__(self, player: Player):
        super().__init__("LessonLearned", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, True, False, player, None, id=44)
        self.description = "Deal 10 damage. If Fatal, Upgrade a random card in your deck. Exhaust."
        self.listener = Listener(Listener.Event.END_COMBAT, self.do_upgrade_card)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 10(13) damage. If {{Fatal}}, {{Upgrade}} a random card in your deck. {{Exhaust}}.
        if not target_enemy.minion and not target_enemy.is_alive():
            player.add_listener(self.listener)

        return True

    def do_upgrade_card(self, player, enemy, enemies, debug):
        random.choice(player.deck.get_deck([self])).upgrade()

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 13 damage. If Fatal, Upgrade a random card in your deck. Exhaust."
        self.damage = 13
