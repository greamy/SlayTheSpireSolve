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
from Actions.Library.ConjureBlade import ConjureBlade
from Actions.Library.Crescendo import Crescendo
from Actions.Library.CrushJoints import CrushJoints
from Actions.Library.DeceiveReality import DeceiveReality
from Actions.Library.Defend import Defend
from Actions.Library.DevaForm import DevaForm
from Actions.Library.Expunger import Expunger
from Actions.Library.Omega import Omega
from Actions.Library.Safety import Safety
from Actions.Library.Smite import Smite
from Actions.Library.Miracle import Miracle
from Actions.Library.Conclude import Conclude
from Actions.Library.Consecrate import Consecrate
from Actions.Library.Strike import Strike
from Actions.Listener import Listener
from Actions.Library.CutThroughFate import CutThroughFate
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
        self.assertIn(card, self.player.deck.used_powers)
        self.assertEqual(len(self.player.listeners), 1)

        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-50)

    def test_battle_hymn(self):
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        card = BattleHymn()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.used_powers)

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
        # Deal 7(10) damage for each enemy in combat.
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
        # Deal 12(16) damage. Deals additional damage for all {{Mantra}} gained this combat.
        card = Brilliance()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 12)

        self.enemy.health = self.enemy_start_health

        self.player.add_mantra(5)
        self.assertEqual(self.player.mantra, 5)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (12+self.player.mantra))

        self.enemy.health = self.enemy_start_health * 3

        self.player.deck.hand.append(card)
        self.player.add_mantra(10)
        self.assertEqual(self.player.get_mantra_count(), 5)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health*3 - (12 + self.player.mantra) * 3)

    def test_CarveReality(self):
        # Deal 6(10) damage. Add a {{C|Smite}} into your hand.
        card = CarveReality()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[0], Smite)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.enemy_start_health-6, self.enemy.health)

    def test_Collect(self):
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.
        card = Collect()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 0)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[0], Miracle)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand),3)

        self.assertIsInstance(self.player.deck.hand[1], Miracle)
        self.assertIsInstance(self.player.deck.hand[2], Miracle)

        self.player.deck.hand.clear()

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 0)



    def test_Miracle(self):
        # Retain. Gain 1(2) energy. {{Exhaust}}.
        card = Miracle()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 4)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, False)
        self.assertIn(card, self.player.deck.hand)

    def test_Conclude(self):
        # Deal 12(16) damage to ALL enemies. End your turn.
        card = Conclude()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.enemies.append(copy.deepcopy(self.enemy))

        for enemy in self.enemies:
            self.assertEqual(enemy.health, self.enemy_start_health-12)

        self.assertTrue(self.player.turn_over)

    def test_ConjureBlade(self):
        # Shuffle an {{C|Expunger}} with X(+1) attacks into your draw pile. {{Exhaust}}.
        energy = self.player.energy
        card = ConjureBlade()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.draw_pile[0], Expunger)
        self.assertEqual(self.player.energy, 0)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(self.player.deck.draw_pile[0].attacks, energy)

    def test_Expunger(self):
        # Deal 9 damage X times.
        energy_used = 3
        card = Expunger(energy_used)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(energy_used*9))

    def test_Consecrate(self):
        # Deal 5(8) damage to all enemies.
        card = Consecrate()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-5)

        self.enemy.health = self.enemy_start_health
        self.enemies.append(copy.deepcopy(self.enemy))

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health-5)
        self.assertEqual(self.enemies[1].health, self.enemy_start_health-5)

    def test_Crescendo(self):
        # {{Retain}}. Enter {{Wrath}}. {{Exhaust}}.
        card = Crescendo()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.stance, Player.Stance.WRATH)
        self.assertIn(card, self.player.deck.exhaust_pile)

        card = Crescendo()
        self.player.deck.hand.append(card)
        self.player.deck.end_turn(debug=False)
        self.assertIn(card, self.player.deck.hand)

    def test_CrushJoints(self):
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.

        card = CrushJoints(self.player)
        self.player.deck.hand.append(card)
        skill = Defend()
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, False)
        self.assertTrue(card.skill_played)

        attack = Strike()
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, False)
        self.assertFalse(card.skill_played)

        self.enemy.health = self.enemy_start_health

        skill = Defend()
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, False)

        self.player.energy = 3

        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertFalse(card.skill_played)
        self.assertEqual(self.enemy.health, self.enemy_start_health-8)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)

        attack = Strike()
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (1.5*6) - 8)

        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.0)

    def test_CutThroughFate(self):
        draw_pile = [Strike(), Defend(), Strike()]
        card = CutThroughFate()
        self.player.deck.hand.append(card)
        self.player.deck.draw_pile.extend(draw_pile)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-7)
        self.assertEqual(len(self.player.deck.hand), 1)

    def test_DeceiveReality(self):
        card = DeceiveReality()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, 4)
        self.assertIsInstance(self.player.deck.hand[0], Safety)
        self.assertEqual(len(self.player.deck.discard_pile), 1)

    def test_Safety(self):
        card = Safety()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.deck.end_turn(False)
        self.assertIn(card, self.player.deck.hand)

    def test_defend(self):
        card = Defend()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.player.block, 5)

    def test_DevaForm(self):
        card = DevaForm()
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.energy = 3
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        print(self.player.energy)







if __name__ == '__main__':
    unittest.main()
