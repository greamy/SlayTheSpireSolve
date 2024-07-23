import unittest

from Actions.Intent import Intent
from Actions.Library.Alpha import Alpha
from Actions.Library.BattleHymn import BattleHymn
from Actions.Library.Beta import Beta
from Actions.Library.Blasphemy import Blasphemy
from Actions.Library.BowlingBash import BowlingBash
from Actions.Library.Brilliance import Brilliance
from Actions.Library.CarveReality import CarveReality
from Actions.Library.Collect import Collect
from Actions.Library.Omega import Omega
from Actions.Library.Smite import Smite
from Actions.Library.Miracle import Miracle
from Actions.Listener import Listener
from Entities.Enemy import Enemy
from Entities.Player import Player
import copy



class CardTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.player = Player(self.health, [], self.energy, self.gold, [], [], [])
        self.enemy_start_health = 51
        self.enemy = Enemy(health=self.enemy_start_health, status_list=[], intent_set=[Intent(12, 1, 0, "", 25),
                                                                         Intent(7, 1, 5, "", 30),
                                                                         Intent(5, 1, 9, "", 45)])
        self.enemies = [self.enemy]

    def test_alpha(self):
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        card = Alpha()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Beta)

    def test_beta(self):
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        card = Beta()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Omega)

    def test_omega(self):
        # At the end of your turn, deal 50 damage to ALL enemies.
        card = Omega()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(len(self.player.listeners), 1)

        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-50)

    def test_battle_hymn(self):
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        card = BattleHymn()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[0], Smite)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[1], Smite)

    def test_smite(self):
        # Retain. Deal 12 damage. {{Exhaust}}.
        card = Smite()
        self.player.deck.hand.append(card)
        self.player.deck.end_turn(False)
        self.assertIn(card, self.player.deck.hand)
        self.assertNotIn(card, self.player.deck.discard_pile)

        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-12)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertNotIn(card, self.player.deck.hand)

    def test_blasphemy(self):
        # (Retain.) Enter Divinity, Die next turn. {{Exhaust}}.
        card = Blasphemy()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(len(self.player.listeners), 1)

        # Make sure 1_000_000 health is enough to survive
        self.player.health = 1_000_000
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertTrue(self.player.is_alive())

        # Ensure listener removes itself after one turn
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertTrue(self.player.is_alive())

        # Ensure card kills player when played a second time
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertFalse(self.player.is_alive())

    def test_bowlingbash(self):
        card = BowlingBash()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-7)

        self.enemy.health = self.enemy_start_health

        self.enemies.append(copy.deepcopy(self.enemy))
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(7*len(self.enemies)))

    def test_brilliance(self):
        card = Brilliance()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 12)

        self.enemy.health = self.enemy_start_health

        self.player.add_mantra(5)
        self.assertEqual(self.player.mantra, 5)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (12+self.player.total_mantra))

        self.enemy.health = self.enemy_start_health * 3

        self.player.deck.hand.append(card)
        self.player.add_mantra(10)
        self.assertEqual(self.player.mantra, 5)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health*3 - (12 + self.player.total_mantra) * 3)

    def test_CarveReality(self):
        card = CarveReality()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertIn(card, self.player.deck.discard_pile)
        self.assertIn(Smite, self.player.deck.hand)
        self.assertEqual(self.enemy_start_health-6, self.enemy.health)

    def test_Collect(self):
        card = Collect()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 0)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertIn(Miracle, self.player.deck.hand)
        self.assertEqual(self.player.energy, 3)

    def test_Miracle(self):
        card = Miracle()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 4)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, False)
        self.assertIn(card, self.player.deck.hand)










if __name__ == '__main__':
    unittest.main()
