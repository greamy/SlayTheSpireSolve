import unittest
from Actions.Card import Card
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Intent import Intent
from Combat import Combat


class CombatTest(unittest.TestCase):

    def setUp(self):
        self.cards = [
            Card(name="Strike" + str(i), energy=1, damage=6, attacks=1, block=0, draw=0, discard=0, exhaust=False,
                 status="none", stance=None) for i in range(5)]
        self.cards.extend(
            Card(name="Defend" + str(i), energy=1, damage=0, attacks=0, block=5, draw=0, discard=0, exhaust=False,
                 status="none", stance=None) for i in range(5))

        self.player = Player(health=69, status_list=[], energy=3, gold=690, potions=[], relics=[],
                             cards=self.cards)

        self.enemy = Enemy(health=42, status_list=[], intent_set=[Intent(0, 0, 5, "", 100)])

    def test_basic_combat(self):
        combat = Combat(self.player, [self.enemy])
        num_turns, player_health, is_alive = combat.start()
        self.assertEqual(combat.get_total_enemy_health(), 0)

    def test_multiple_enemies(self):
        enemy2 = Enemy(health=42, status_list=[], intent_set=[Intent(5, 1, 0, "", 100)])
        combat = Combat(self.player, [self.enemy, enemy2])
        num_turns, player_health, is_alive = combat.start()
        if player_health > 0:
            self.assertEqual(combat.get_total_enemy_health(), 0)
        else:
            self.assertFalse(is_alive)
