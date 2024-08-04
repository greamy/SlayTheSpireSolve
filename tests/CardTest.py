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
from Actions.Library.Devotion import Devotion
from Actions.Library.EmptyFist import EmptyFist
from Actions.Library.EmptyMind import EmptyMind
from Actions.Library.Eruption import Eruption
from Actions.Library.Establishment import Establishment
from Actions.Library.Evaluate import Evaluate
from Actions.Library.Expunger import Expunger
from Actions.Library.FearNoEvil import FearNoEvil
from Actions.Library.FlurryofBlows import FlurryofBlows
from Actions.Library.FlyingSleeves import FlyingSleeves
from Actions.Library.FollowUp import FollowUp
from Actions.Library.Halt import Halt
from Actions.Library.Indignation import Indignation
from Actions.Library.InnerPeace import InnerPeace
from Actions.Library.Insight import Insight
from Actions.Library.Judgment import Judgment
from Actions.Library.JustLucky import JustLucky
from Actions.Library.LessonLearned import LessonLearned
from Actions.Library.LikeWater import LikeWater
from Actions.Library.MasterReality import MasterReality
from Actions.Library.Meditate import Meditate
from Actions.Library.MentalFortress import MentalFortress
from Actions.Library.Nirvana import Nirvana
from Actions.Library.Omega import Omega
from Actions.Library.Omniscience import Omniscience
from Actions.Library.Perseverance import Perseverance
from Actions.Library.Pray import Pray
from Actions.Library.PressurePoints import PressurePoints
from Actions.Library.Prostrate import Prostrate
from Actions.Library.Protect import Protect
from Actions.Library.Ragnarok import Ragnarok
from Actions.Library.ReachHeaven import ReachHeaven
from Actions.Library.Rushdown import Rushdown
from Actions.Library.Safety import Safety
from Actions.Library.Sanctity import Sanctity
from Actions.Library.Smite import Smite
from Actions.Library.Miracle import Miracle
from Actions.Library.Conclude import Conclude
from Actions.Library.Consecrate import Consecrate
from Actions.Library.Strike import Strike
from Actions.Library.ThroughViolence import ThroughViolence
from Actions.Listener import Listener
from Actions.Library.CutThroughFate import CutThroughFate
from Actions.Library.EmptyBody import EmptyBody
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
        self.enemy = Enemy(health=self.enemy_start_health, status_list=[], intent_set=[Intent(12, 1, 0, 25),
                                                                         Intent(7, 1, 5, 30),
                                                                         Intent(5, 1, 9, 45)])
        self.enemies = [self.enemy]

    def test_alpha(self):
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        card = Alpha(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Beta)

    def test_beta(self):
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        card = Beta(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Omega)

    def test_omega(self):
        # At the end of your turn, deal 50 damage to ALL enemies.
        card = Omega(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.used_powers)
        self.assertEqual(len(self.player.listeners), 1)

        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-50)

    def test_battle_hymn(self):
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        card = BattleHymn(self.player)
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
        card = Smite(self.player)
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
        card = Blasphemy(self.player)
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
        card = BowlingBash(self.player)
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
        card = Brilliance(self.player)
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
        card = CarveReality(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[0], Smite)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.enemy_start_health-6, self.enemy.health)

    def test_Collect(self):
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.
        card = Collect(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 0)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertIsInstance(self.player.deck.hand[0], Miracle)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 3)

        self.assertIsInstance(self.player.deck.hand[1], Miracle)
        self.assertIsInstance(self.player.deck.hand[2], Miracle)

        self.player.deck.hand.clear()

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 0)

    def test_Miracle(self):
        # Retain. Gain 1(2) energy. {{Exhaust}}.
        card = Miracle(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.assertEqual(self.player.energy, 4)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, False)
        self.assertIn(card, self.player.deck.hand)

    def test_Conclude(self):
        # Deal 12(16) damage to ALL enemies. End your turn.
        card = Conclude(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.enemies.append(copy.deepcopy(self.enemy))

        for enemy in self.enemies:
            self.assertEqual(enemy.health, self.enemy_start_health-12)

        self.assertTrue(self.player.turn_over)

    def test_ConjureBlade(self):
        # Shuffle an {{C|Expunger}} with X(+1) attacks into your draw pile. {{Exhaust}}.
        energy = self.player.energy
        card = ConjureBlade(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.draw_pile[0], Expunger)
        self.assertEqual(self.player.energy, 0)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(self.player.deck.draw_pile[0].attacks, energy)

    def test_Expunger(self):
        # Deal 9 damage X times.
        energy_used = 3
        card = Expunger(self.player, energy_used)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(energy_used*9))

    def test_Consecrate(self):
        # Deal 5(8) damage to all enemies.
        card = Consecrate(self.player)
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
        card = Crescendo(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.stance, Player.Stance.WRATH)
        self.assertIn(card, self.player.deck.exhaust_pile)

        card = Crescendo(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.end_turn(debug=False)
        self.assertIn(card, self.player.deck.hand)

    def test_CrushJoints(self):
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.

        card = CrushJoints(self.player)
        self.player.deck.hand.append(card)
        skill = Defend(self.player)
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, False)
        self.assertTrue(card.skill_played)

        attack = Strike(self.player)
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, False)
        self.assertFalse(card.skill_played)

        self.enemy.health = self.enemy_start_health

        skill = Defend(self.player)
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, False)

        self.player.energy = 3

        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertFalse(card.skill_played)
        self.assertEqual(self.enemy.health, self.enemy_start_health-8)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)

        attack = Strike(self.player)
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (1.5*6) - 8)

        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.0)

    def test_CutThroughFate(self):
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.
        draw_pile = [Strike(self.player), Defend(self.player), Strike(self.player)]
        card = CutThroughFate(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.draw_pile.extend(draw_pile)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-7)
        self.assertEqual(len(self.player.deck.hand), 1)

    def test_DeceiveReality(self):
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.
        card = DeceiveReality(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, 4)
        self.assertIsInstance(self.player.deck.hand[0], Safety)
        self.assertEqual(len(self.player.deck.discard_pile), 1)

    def test_Safety(self):
        # {{Retain}}. Gain 12(16) {{Block}}.
        card = Safety(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.deck.end_turn(False)
        self.assertIn(card, self.player.deck.hand)

    def test_defend(self):
        # Gain 5(8) {{Block}}.
        card = Defend(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.player.block, 5)

    def test_DevaForm(self):
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)
        card = DevaForm(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.energy = 3
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.player.energy, 4)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.player.energy, 6)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.player.energy, 9)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.player.deck.exhaust_pile[0], card)

    def test_Devotion(self):
        # At the start of your turn, gain 2(3) {{Mantra}}.
        card = Devotion(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.player.mantra, 2)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.player.get_mantra_count(), 0)
        self.assertEqual(self.player.stance, Player.Stance.DIVINITY)

    def test_EmptyBody(self):
        # Gain 7(10) {{Block}}. Exit your {{Stance}}.
        card = EmptyBody(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, 7)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, 14)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, 3)

    def test_EmptyFist(self):
        # Deal 9(14) damage. Exit your {{Stance}}.
        card = EmptyFist(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy_start_health - 9, self.enemy.health)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 18)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, 3)

    def test_EmptyMind(self):
        # Exit your {{Stance}}. Draw 2(3) cards.
        card = EmptyMind(self.player)
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 2)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 4)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, 3)

    def test_Eruption(self):
        # Deal 9 damage. Enter {{Wrath}}.
        card = Eruption(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-9)
        self.assertEqual(self.player.stance, self.player.Stance.WRATH)

    def test_Establishment(self):
        # ({{Innate}}.) Whenever a card is {{Retained}}, lower its cost by 1.
        card = Establishment(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.player.deck.hand.append(Safety(self.player))
        self.player.end_turn(self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 1)
        self.assertEqual(self.player.deck.hand[0].energy, 0)

    def test_Evaluate(self):
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.
        card = Evaluate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.draw_pile[0], Insight)
        self.assertEqual(self.player.block, 6)

    def test_Insight(self):
        # {{Retain}} Draw 2(3) cards}. {{Exhaust}}
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        card = Insight(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 2)
        self.assertIn(card, self.player.deck.exhaust_pile)

    def test_FearNoEvil(self):
        # Deal 8(11) damage. If the enemy intends to Attack, enter {{Calm}}.
        card = FearNoEvil(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertEqual(self.player.stance, Player.Stance.CALM)

    def test_FlyingSleeves(self):
        # {{Retain}}. Deal 4(6) damage twice.
        card = FlyingSleeves(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-8)

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, False)
        self.assertIn(card, self.player.deck.hand)

    def test_FollowUp(self):
        # Deal 7(11) damage. If the previous card played was an Attack, gain 1 {{Energy}}.
        card = FollowUp(self.player)
        self.player.deck.hand.append(card)
        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, False)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 6 - 7)
        self.assertEqual(self.player.energy, 2)

    def test_FlurryOfBlows(self):
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.
        card = FlurryofBlows(self.player)
        new_card = FlurryofBlows(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.player.deck.draw_pile.append(new_card)
        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.assertIn(new_card, self.player.deck.draw_pile)
        self.assertIn(card, self.player.deck.hand)

        self.player.play_card(card, self.enemy, self.enemies, False)

        Empty_fist = EmptyFist(self.player)
        self.player.deck.hand.append(Empty_fist)
        self.player.play_card(Empty_fist, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 1)

    def test_Halt(self):
        # Gain 3(4) {{Block}}. {{Wrath}}: Gain 9(14) additional {{Block}}.
        card = Halt(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.player.block = 0

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block + card.wrath_block)

    def test_Indignation(self):
        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.
        card = Indignation(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.stance, self.player.Stance.WRATH)

        crescendo = Crescendo(self.player)
        self.player.deck.hand.append(crescendo)
        self.player.play_card(crescendo, self.enemy, self.enemies, False)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, False)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.0)

    def test_InnerPeace(self):
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player), Strike(self.player)])
        card = InnerPeace(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.stance, self.player.Stance.CALM)
        self.assertEqual(len(self.player.deck.draw_pile), 3)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.hand), 3)

    def test_Judgement(self):
        # If the enemy has 30(40) or less HP, set their HP to 0.
        card = Judgment(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health)

        self.enemy.health = 30
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertFalse(self.enemy.is_alive())

    def test_JustLucky(self):
        card = JustLucky(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

    def test_LessonLearned(self):
        card = LessonLearned(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.player.deck.exhaust_pile.clear()

        self.enemy.health = 10
        self.player.energy = 3

        card = LessonLearned(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertFalse(self.enemy.is_alive())
        self.assertTrue(card.upgraded)

    def test_LikeWater(self):
        card = LikeWater(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.player.block, 0)

        self.player.stance = Player.Stance.CALM
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, False)
        self.assertEqual(self.player.block, card.end_turn_block)

    def test_MasterReality(self):
        # Whenever a card is created during combat, {{Upgrade}} it.
        card = MasterReality(self.player)
        alpha = Alpha(self.player)

        self.player.deck.hand.append(card)
        self.player.deck.hand.append(alpha)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.player.play_card(alpha, self.enemy, self.enemies, False)

        self.assertTrue(self.player.deck.draw_pile[0].upgraded)

    def test_Meditate(self):
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
        card = Meditate(self.player)
        strike = Strike(self.player)
        self.player.deck.discard_pile.append(strike)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.discard_pile), 1)
        self.assertIn(strike, self.player.deck.hand)

    def test_MentalFortress(self):
        # Whenever you switch {{Stance|Stances}}, gain 4(6) {{Block}}.
        card = MentalFortress(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.stance_block)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.stance_block)

    def test_Nirvana(self):
        # Whenever you {{Scry}}, gain 3(4) {{Block}}.
        card = Nirvana(self.player)
        ctf = CutThroughFate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)

        self.player.deck.hand.append(ctf)
        self.player.play_card(ctf, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.scry_block)

    def test_Omniscience(self):
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. {{Exhaust}}.
        self.player.energy = 4
        card = Omniscience(self.player)
        strike = Strike(self.player)
        self.player.deck.draw_pile.append(strike)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(strike.damage*2))

    def test_Perseverance(self):
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retained}}, increase its {{Block}} by 2(3).
        card = Perseverance(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)

        self.player.block = 0

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, False)
        self.assertEqual(card.block, 7)

    def test_Pray(self):
        # Gain 3(4) {{Mantra}}. Shuffle an {{C|Insight}} into your draw pile.
        card = Pray(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertIsInstance(self.player.deck.draw_pile[0], Insight)
        self.assertEqual(self.player.mantra, 3)

    def test_TheMostOverratedCard_PressurePoints(self):
        # Apply 8(11) Mark. ALL enemies lose HP equal to their Mark.
        self.enemies.append(copy.deepcopy(self.enemy))
        card = PressurePoints(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, False)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health-self.enemy.mark)
        self.enemy.block = 10000000
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, False)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health - card.card_mark*3)

        self.enemies[0].health = self.enemy_start_health
        self.player.energy = 3
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[1], self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.card_mark * 2)
        self.assertEqual(self.enemies[1].health, self.enemy_start_health - card.card_mark * 1)

    def test_Prostate(self):
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.
        card = Prostrate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)
        self.assertEqual(self.player.mantra, card.mantra)

    def test_Protect(self):
        # {{Retain}}. Gain 12(16) {{Block}}.
        card = Protect(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)
        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, False)
        self.assertIn(card, self.player.deck.hand)

    def test_Ragnarok(self):
        # Deal 5(6) damage to a random enemy 5(6) times.
        card = Ragnarok(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage*card.attacks)
        self.enemies[0].health = self.enemy_start_health
        self.enemies.append(copy.deepcopy(self.enemy))
        self.player.energy = 3
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, False)
        self.assertEqual((self.enemies[0].health + self.enemies[1].health), self.enemy_start_health * 2 - card.damage * card.attacks)

    def test_ReachHeaven(self):
        # Deal 10(15) damage. Shuffle a {{C|Through Violence}} into your draw pile.
        card = ReachHeaven(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertIsInstance(self.player.deck.draw_pile[0], ThroughViolence)

    def test_ThroughViolence(self):
        card = ThroughViolence(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, False)
        self.assertIn(card, self.player.deck.hand)

    def test_Rushdown(self):
        # Whenever you enter {{Wrath}}, draw 2 cards.
        card = Rushdown(self.player)
        self.player.deck.draw_pile.extend([Strike(self.player), Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)
        self.player.energy = 3
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)



    def test_Sanctity(self):
        # Gain 6(9) {{Block}}. If the previous card played was a Skill, draw 2 card.
        card = Sanctity(self.player)
        self.player.deck.draw_pile.extend([Strike(self.player), Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(self.player.block, card.block)

        defend = Defend(self.player)
        self.player.deck.hand.append(defend)
        self.player.play_card(defend, self.enemy, self.enemies, False)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, False)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)















if __name__ == '__main__':
    unittest.main()
