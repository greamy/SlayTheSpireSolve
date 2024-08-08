import random
import unittest

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Alpha import Alpha
from CombatSim.Actions.Library.BattleHymn import BattleHymn
from CombatSim.Actions.Library.Beta import Beta
from CombatSim.Actions.Library.Blasphemy import Blasphemy
from CombatSim.Actions.Library.BowlingBash import BowlingBash
from CombatSim.Actions.Library.Brilliance import Brilliance
from CombatSim.Actions.Library.CarveReality import CarveReality
from CombatSim.Actions.Library.Collect import Collect
from CombatSim.Actions.Library.ConjureBlade import ConjureBlade
from CombatSim.Actions.Library.Crescendo import Crescendo
from CombatSim.Actions.Library.CrushJoints import CrushJoints
from CombatSim.Actions.Library.DeceiveReality import DeceiveReality
from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.DevaForm import DevaForm
from CombatSim.Actions.Library.Devotion import Devotion
from CombatSim.Actions.Library.EmptyFist import EmptyFist
from CombatSim.Actions.Library.EmptyMind import EmptyMind
from CombatSim.Actions.Library.Eruption import Eruption
from CombatSim.Actions.Library.Establishment import Establishment
from CombatSim.Actions.Library.Evaluate import Evaluate
from CombatSim.Actions.Library.Expunger import Expunger
from CombatSim.Actions.Library.FearNoEvil import FearNoEvil
from CombatSim.Actions.Library.FlurryofBlows import FlurryofBlows
from CombatSim.Actions.Library.FlyingSleeves import FlyingSleeves
from CombatSim.Actions.Library.FollowUp import FollowUp
from CombatSim.Actions.Library.Halt import Halt
from CombatSim.Actions.Library.Indignation import Indignation
from CombatSim.Actions.Library.InnerPeace import InnerPeace
from CombatSim.Actions.Library.Insight import Insight
from CombatSim.Actions.Library.Judgment import Judgment
from CombatSim.Actions.Library.JustLucky import JustLucky
from CombatSim.Actions.Library.LessonLearned import LessonLearned
from CombatSim.Actions.Library.LikeWater import LikeWater
from CombatSim.Actions.Library.MasterReality import MasterReality
from CombatSim.Actions.Library.Meditate import Meditate
from CombatSim.Actions.Library.MentalFortress import MentalFortress
from CombatSim.Actions.Library.Nirvana import Nirvana
from CombatSim.Actions.Library.Omega import Omega
from CombatSim.Actions.Library.Omniscience import Omniscience
from CombatSim.Actions.Library.Perseverance import Perseverance
from CombatSim.Actions.Library.Pray import Pray
from CombatSim.Actions.Library.PressurePoints import PressurePoints
from CombatSim.Actions.Library.Prostrate import Prostrate
from CombatSim.Actions.Library.Protect import Protect
from CombatSim.Actions.Library.Ragnarok import Ragnarok
from CombatSim.Actions.Library.ReachHeaven import ReachHeaven
from CombatSim.Actions.Library.Rushdown import Rushdown
from CombatSim.Actions.Library.Safety import Safety
from CombatSim.Actions.Library.Sanctity import Sanctity
from CombatSim.Actions.Library.SandsofTime import SandsofTime
from CombatSim.Actions.Library.SashWhip import SashWhip
from CombatSim.Actions.Library.Scrawl import Scrawl
from CombatSim.Actions.Library.SignatureMove import SignatureMove
from CombatSim.Actions.Library.SimmeringFury import SimmeringFury
from CombatSim.Actions.Library.Smite import Smite
from CombatSim.Actions.Library.SpiritShield import SpiritShield
from CombatSim.Actions.Library.Miracle import Miracle
from CombatSim.Actions.Library.Conclude import Conclude
from CombatSim.Actions.Library.Consecrate import Consecrate
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Actions.Library.Study import Study
from CombatSim.Actions.Library.Swivel import Swivel
from CombatSim.Actions.Library.TalktotheHand import TalktotheHand
from CombatSim.Actions.Library.Tantrum import Tantrum
from CombatSim.Actions.Library.ThirdEye import ThirdEye
from CombatSim.Actions.Library.ThroughViolence import ThroughViolence
from CombatSim.Actions.Library.Tranquility import Tranquility
from CombatSim.Actions.Library.Vault import Vault
from CombatSim.Actions.Library.Vigilance import Vigilance
from CombatSim.Actions.Library.Wallop import Wallop
from CombatSim.Actions.Library.WaveoftheHand import WaveoftheHand
from CombatSim.Actions.Library.Weave import Weave
from CombatSim.Actions.Library.WheelKick import WheelKick
from CombatSim.Actions.Library.WindmillStrike import WindmillStrike
from CombatSim.Actions.Library.Wish import Wish
from CombatSim.Actions.Library.Worship import Worship
from CombatSim.Actions.Library.WreathofFlame import WreathofFlame
from CombatSim.Actions.Listener import Listener
from CombatSim.Actions.Library.CutThroughFate import CutThroughFate
from CombatSim.Actions.Library.EmptyBody import EmptyBody
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
import copy


class CardTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.player = Player(self.health, self.energy, self.gold, [], [], [])
        self.enemy_start_health = 51
        self.enemy = Enemy(health=self.enemy_start_health, status_list=[], intent_set=[Intent(12, 1, 0, 25),
                                                                         Intent(7, 1, 5, 30),
                                                                         Intent(5, 1, 9, 45)])
        self.enemies = [self.enemy]
        self.debug = False

    def test_alpha(self):
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        card = Alpha(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Beta)

    def test_beta(self):
        # Shuffle an {{C|Omega}} into your draw pile. {{Exhaust}}.
        card = Beta(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertIsInstance(self.player.deck.draw_pile[0], Omega)

    def test_omega(self):
        # At the end of your turn, deal 50 damage to ALL enemies.
        card = Omega(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.used_powers)
        self.assertEqual(len(self.player.listeners), 1)

        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-50)

    def test_battle_hymn(self):
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        card = BattleHymn(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.used_powers)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.hand[0], Smite)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.hand[1], Smite)

    def test_smite(self):
        # Retain. Deal 12 damage. {{Exhaust}}.
        card = Smite(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.end_turn(self.debug)
        self.assertIn(card, self.player.deck.hand)
        self.assertNotIn(card, self.player.deck.discard_pile)

        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertNotIn(card, self.player.deck.hand)

    def test_blasphemy(self):
        # (Retain.) Enter Divinity, Die next turn. {{Exhaust}}.
        card = Blasphemy(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(len(self.player.listeners), 1)

        # Make sure 1_000_000 health is enough to survive
        self.player.health = 1_000_000
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertTrue(self.player.is_alive())

        # Ensure listener removes itself after one turn
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertTrue(self.player.is_alive())

        # Ensure card kills player when played a second time
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertFalse(self.player.is_alive())

    def test_BowlingBash(self):
        # Deal 7(10) damage for each enemy in combat.
        card = BowlingBash(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)

        self.enemy.health = self.enemy_start_health

        self.enemies.append(copy.deepcopy(self.enemy))
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(card.damage*len(self.enemies)))

    def test_brilliance(self):
        # Deal 12(16) damage. Deals additional damage for all {{Mantra}} gained this combat.
        card = Brilliance(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.enemy.health = self.enemy_start_health

        mantra = 5
        self.player.add_mantra(mantra)
        self.assertEqual(self.player.mantra, mantra)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.enemy_start_health *= 3
        self.enemy.health = self.enemy_start_health

        self.player.deck.hand.append(card)
        self.player.add_mantra(mantra*2)
        self.assertEqual(self.player.get_mantra_count(), mantra)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage * 3)

    def test_CarveReality(self):
        # Deal 6(10) damage. Add a {{C|Smite}} into your hand.
        card = CarveReality(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.hand[0], Smite)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.enemy_start_health-card.damage, self.enemy.health)

    def test_Collect(self):
        # Put an {{C|Miracle|Miracle+}} into your hand at the start of your next X(+1) turns. {{Exhaust}}.
        card = Collect(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.assertEqual(self.player.energy, self.energy-3)
        self.assertEqual(len(self.player.listeners), 1)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.hand[0], Miracle)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 3)

        self.assertIsInstance(self.player.deck.hand[1], Miracle)
        self.assertIsInstance(self.player.deck.hand[2], Miracle)

        self.player.deck.hand.clear()

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 0)

    def test_Miracle(self):
        # Retain. Gain 1(2) energy. {{Exhaust}}.
        card = Miracle(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.assertEqual(self.player.energy, self.energy - card.energy)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_Conclude(self):
        # Deal 12(16) damage to ALL enemies. End your turn.
        card = Conclude(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.enemies.append(copy.deepcopy(self.enemy))

        for enemy in self.enemies:
            self.assertEqual(enemy.health, self.enemy_start_health-card.damage)

        self.assertTrue(self.player.turn_over)

    def test_ConjureBlade(self):
        # Shuffle an {{C|Expunger}} with X(+1) attacks into your draw pile. {{Exhaust}}.
        energy = self.player.energy
        card = ConjureBlade(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.draw_pile[0], Expunger)
        self.assertEqual(self.player.energy, 0)
        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(self.player.deck.draw_pile[0].attacks, energy)

    def test_Expunger(self):
        # Deal 9 damage X times.
        energy_used = 3
        card = Expunger(self.player, energy_used)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(energy_used*9))

    def test_Consecrate(self):
        # Deal 5(8) damage to all enemies.
        card = Consecrate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)

        self.enemy.health = self.enemy_start_health
        self.enemies.append(copy.deepcopy(self.enemy))

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health-card.damage)
        self.assertEqual(self.enemies[1].health, self.enemy_start_health-card.damage)

    def test_Crescendo(self):
        # {{Retain}}. Enter {{Wrath}}. {{Exhaust}}.
        card = Crescendo(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.stance, Player.Stance.WRATH)
        self.assertIn(card, self.player.deck.exhaust_pile)

        card = Crescendo(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.end_turn(self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_CrushJoints(self):
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.

        card = CrushJoints(self.player)
        self.player.deck.hand.append(card)
        skill = Defend(self.player)
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, self.debug)
        self.assertTrue(card.skill_played)

        attack = Strike(self.player)
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, self.debug)
        self.assertFalse(card.skill_played)

        self.enemy.health = self.enemy_start_health

        skill = Defend(self.player)
        self.player.deck.hand.append(skill)
        self.player.play_card(skill, self.enemy, self.enemies, self.debug)

        self.player.energy = self.energy

        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertFalse(card.skill_played)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)

        attack = Strike(self.player)
        self.player.deck.hand.append(attack)
        self.player.play_card(attack, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (1.5*attack.damage) - card.damage)

        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.0)

    def test_CutThroughFate(self):
        # Deal 7(9) damage. {{Scry}} 2(3). Draw 1 card.
        draw_pile = [Strike(self.player), Defend(self.player), Strike(self.player)]
        card = CutThroughFate(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.draw_pile.extend(draw_pile)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertEqual(len(self.player.deck.hand), card.draw)

    def test_DeceiveReality(self):
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.
        card = DeceiveReality(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)
        self.assertIsInstance(self.player.deck.hand[0], Safety)
        self.assertEqual(len(self.player.deck.discard_pile), 1)

    def test_Safety(self):
        # {{Retain}}. Gain 12(16) {{Block}}.
        card = Safety(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.deck.end_turn(self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_defend(self):
        # Gain 5(8) {{Block}}.
        card = Defend(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.player.block, card.block)

    def test_DevaForm(self):
        # {{Ethereal}}. At the start of your turn, gain {{Energy}} and increase this gain by 1. (not {{Ethereal}}.)
        card = DevaForm(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.energy = self.energy
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.energy + 1)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.energy + 1 + 2)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.energy + 1 + 2 + 3)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.deck.exhaust_pile[0], card)

    def test_Devotion(self):
        # At the start of your turn, gain 2(3) {{Mantra}}.
        card = Devotion(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.mantra, card.mantra)

        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.get_mantra_count(), 0)
        self.assertEqual(self.player.stance, Player.Stance.DIVINITY)

    def test_EmptyBody(self):
        # Gain 7(10) {{Block}}. Exit your {{Stance}}.
        card = EmptyBody(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block*2)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, self.energy)

    def test_EmptyFist(self):
        # Deal 9(14) damage. Exit your {{Stance}}.
        card = EmptyFist(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy_start_health - card.damage, self.enemy.health)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage*2)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, self.energy)

    def test_EmptyMind(self):
        # Exit your {{Stance}}. Draw 2(3) cards.
        card = EmptyMind(self.player)
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), card.draw)

        self.player.set_stance(Player.Stance.CALM)
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), card.draw * 2)
        self.assertEqual(self.player.stance, Player.Stance.NONE)
        self.assertEqual(self.player.energy, self.energy)

    def test_Eruption(self):
        # Deal 9 damage. Enter {{Wrath}}.
        card = Eruption(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertEqual(self.player.stance, self.player.Stance.WRATH)

    def test_Establishment(self):
        # ({{Innate}}.) Whenever a card is {{Retained}}, lower its cost by 1.
        card = Establishment(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.player.deck.hand.append(Safety(self.player))
        self.player.end_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 1)
        self.assertEqual(self.player.deck.hand[0].energy, 0)

    def test_Evaluate(self):
        # Gain 6(10) {{Block}}. Shuffle an {{C|Insight}} into your draw pile.
        card = Evaluate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.draw_pile[0], Insight)
        self.assertEqual(self.player.block, card.block)

    def test_Insight(self):
        # {{Retain}} Draw 2(3) cards}. {{Exhaust}}
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player)])
        card = Insight(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), card.draw)
        self.assertIn(card, self.player.deck.exhaust_pile)

    def test_FearNoEvil(self):
        # Deal 8(11) damage. If the enemy intends to Attack, enter {{Calm}}.
        card = FearNoEvil(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertEqual(self.player.stance, Player.Stance.CALM)

    def test_FlyingSleeves(self):
        # {{Retain}}. Deal 4(6) damage twice.
        card = FlyingSleeves(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(card.damage * card.attacks))

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_FollowUp(self):
        # Deal 7(11) damage. If the previous card played was an Attack, gain 1 {{Energy}}.
        card = FollowUp(self.player)
        self.player.deck.hand.append(card)
        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage - strike.damage)
        self.assertEqual(self.player.energy, self.energy - 1)

    def test_FlurryOfBlows(self):
        # Deal 4(6) damage. On {{Stance}} change, returns from the Discard Pile into your hand.
        card = FlurryofBlows(self.player)
        new_card = FlurryofBlows(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.player.deck.draw_pile.append(new_card)
        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.assertIn(new_card, self.player.deck.draw_pile)
        self.assertIn(card, self.player.deck.hand)

        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        Empty_fist = EmptyFist(self.player)
        self.player.deck.hand.append(Empty_fist)
        self.player.play_card(Empty_fist, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 1)

    def test_Halt(self):
        # Gain 3(4) {{Block}}. {{Wrath}}: Gain 9(14) additional {{Block}}.
        card = Halt(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.player.block = 0

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block + card.wrath_block)

    def test_Indignation(self):
        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.
        card = Indignation(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.stance, self.player.Stance.WRATH)

        crescendo = Crescendo(self.player)
        self.player.deck.hand.append(crescendo)
        self.player.play_card(crescendo, self.enemy, self.enemies, self.debug)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.enemy.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.0)

    def test_InnerPeace(self):
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
        self.player.deck.draw_pile = ([Strike(self.player), Strike(self.player), Strike(self.player)])
        card = InnerPeace(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.stance, self.player.Stance.CALM)
        self.assertEqual(len(self.player.deck.draw_pile), 3)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 3)

    def test_Judgement(self):
        # If the enemy has 30(40) or less HP, set their HP to 0.
        card = Judgment(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health)

        self.enemy.health = 30
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertFalse(self.enemy.is_alive())

    def test_JustLucky(self):
        card = JustLucky(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

    def test_LessonLearned(self):
        card = LessonLearned(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.player.deck.exhaust_pile.clear()

        self.enemy.health = 10
        self.player.energy = 3

        card = LessonLearned(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertFalse(self.enemy.is_alive())
        self.assertTrue(card.upgraded)

    def test_LikeWater(self):
        card = LikeWater(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

        self.player.stance = Player.Stance.CALM
        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.end_turn_block)

    def test_MasterReality(self):
        # Whenever a card is created during combat, {{Upgrade}} it.
        card = MasterReality(self.player)
        alpha = Alpha(self.player)

        self.player.deck.hand.append(card)
        self.player.deck.hand.append(alpha)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.play_card(alpha, self.enemy, self.enemies, self.debug)

        self.assertTrue(self.player.deck.draw_pile[0].upgraded)

    def test_Meditate(self):
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
        card = Meditate(self.player)
        strike = Strike(self.player)
        self.player.deck.discard_pile.append(strike)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.discard_pile), 1)
        self.assertIn(strike, self.player.deck.hand)

    def test_MentalFortress(self):
        # Whenever you switch {{Stance|Stances}}, gain 4(6) {{Block}}.
        card = MentalFortress(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.stance_block)

        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.stance_block)

    def test_Nirvana(self):
        # Whenever you {{Scry}}, gain 3(4) {{Block}}.
        card = Nirvana(self.player)
        ctf = CutThroughFate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.player.deck.hand.append(ctf)
        self.player.play_card(ctf, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.scry_block)

    def test_Omniscience(self):
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. {{Exhaust}}.
        self.player.energy = 4
        card = Omniscience(self.player)
        strike = Strike(self.player)
        self.player.deck.draw_pile.append(strike)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(strike.damage*2))

    def test_Perseverance(self):
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retained}}, increase its {{Block}} by 2(3).
        card = Perseverance(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)

        self.player.block = 0

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, self.debug)
        self.assertEqual(card.block, 7)

    def test_Pray(self):
        # Gain 3(4) {{Mantra}}. Shuffle an {{C|Insight}} into your draw pile.
        card = Pray(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.draw_pile[0], Insight)
        self.assertEqual(self.player.mantra, 3)

    def test_TheMostOverratedCard_PressurePoints(self):
        # Apply 8(11) Mark. ALL enemies lose HP equal to their Mark.
        self.enemies.append(copy.deepcopy(self.enemy))
        card = PressurePoints(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, self.debug)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health-self.enemy.mark)
        self.enemy.block = 10000000
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, self.debug)
        self.assertEqual(self.enemies[0].health, self.enemy_start_health - card.card_mark*3)

        self.enemies[0].health = self.enemy_start_health
        self.player.energy = 3
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[1], self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.card_mark * 2)
        self.assertEqual(self.enemies[1].health, self.enemy_start_health - card.card_mark * 1)

    def test_Prostate(self):
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.
        card = Prostrate(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)
        self.assertEqual(self.player.mantra, card.mantra)

    def test_Protect(self):
        # {{Retain}}. Gain 12(16) {{Block}}.
        card = Protect(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)
        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_Ragnarok(self):
        # Deal 5(6) damage to a random enemy 5(6) times.
        card = Ragnarok(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage*card.attacks)
        self.enemies[0].health = self.enemy_start_health
        self.enemies.append(copy.deepcopy(self.enemy))
        self.player.energy = 3
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemies[0], self.enemies, self.debug)
        self.assertEqual((self.enemies[0].health + self.enemies[1].health), self.enemy_start_health * 2 - card.damage * card.attacks)

    def test_ReachHeaven(self):
        # Deal 10(15) damage. Shuffle a {{C|Through Violence}} into your draw pile.
        card = ReachHeaven(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertIsInstance(self.player.deck.draw_pile[0], ThroughViolence)

    def test_ThroughViolence(self):
        card = ThroughViolence(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_Rushdown(self):
        # Whenever you enter {{Wrath}}, draw 2 cards.
        card = Rushdown(self.player)
        self.player.deck.draw_pile.extend([Strike(self.player), Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        eruption = Eruption(self.player)
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)
        self.player.energy = 3
        self.player.deck.hand.append(eruption)
        self.player.play_card(eruption, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)

    def test_Sanctity(self):
        # Gain 6(9) {{Block}}. If the previous card played was a Skill, draw 2 card.
        card = Sanctity(self.player)
        self.player.deck.draw_pile.extend([Strike(self.player), Strike(self.player), Strike(self.player)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)

        defend = Defend(self.player)
        self.player.deck.hand.append(defend)
        self.player.play_card(defend, self.enemy, self.enemies, self.debug)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.draw_pile), 1)
        self.assertEqual(len(self.player.deck.hand), 2)

    def test_SandsOfTime(self):
        # {{Retain}}. Deal 20(26) damage. Whenever this card is {{Retained}}, lower its cost by 1.
        self.player.energy = 4
        card = SandsofTime(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, self.debug)
        self.assertEqual(card.energy, 3)

    def test_SashWhip(self):
        # Deal 8(10) damage. If the last card played this combat was an Attack, apply 1(2) {{Weak}}.
        card = SashWhip(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertTrue(self.enemy.health, self.enemy_start_health-card.damage)

        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)

        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_dealt_multiplier, 1*0.75)

    def test_Scrawl(self):
        # Draw cards until your hand is full. {{Exhaust}}.
        card = Scrawl(self.player)
        self.player.deck.draw_pile.extend([Strike(self.player) for i in range(12)])
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 10)
        self.assertIn(card, self.player.deck.exhaust_pile)

    def test_SignatureMove(self):
        # Can only be played if this is the only attack in your hand. Deal 30(40) damage.
        card = SignatureMove(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.player.deck.hand.append(card)
        self.player.deck.hand.append(Strike(self.player))
        self.player.notify_listeners(Listener.Event.HAND_CHANGED, self.enemies, self.debug)
        self.player.energy = 3
        self.assertFalse(self.player.play_card(card, self.enemy, self.enemies, self.debug))

    def test_SimmeringFury(self):
        # At the start of your next turn, enter {{Wrath}} and draw 2(3) cards.
        card = SimmeringFury(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.player.deck.draw_pile.extend([Strike(self.player) for i in range(2)])
        self.player.notify_listeners(Listener.Event.START_TURN, self.enemies, self.debug)

        self.assertEqual(self.player.stance, Player.Stance.WRATH)
        self.assertEqual(len(self.player.deck.hand), 2)

    def test_SpiritShield(self):
        # Gain 3(4) {{Block}} for each card in your hand.
        card = SpiritShield(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

        self.player.deck.hand.extend([Strike(self.player) for i in range(2)])
        self.player.deck.hand.append(card)
        self.player.energy = 100
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.card_block * 2)

    def test_strike(self):
        # Deal 6(9) damage.
        card = Strike(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)

    def test_Study(self):
        # At the end of your turn, shuffle an {{C|Insight}} into your draw pile.
        card = Study(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.player.notify_listeners(Listener.Event.END_TURN, self.enemies, self.debug)
        self.assertIsInstance(self.player.deck.draw_pile[0], Insight)

    def test_Swivel(self):
        # Gain 8(11) {{Block}}. The next Attack you play costs 0.
        card = Swivel(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block)

        self.player.energy = self.energy
        self.player.notify_listeners(Listener.Event.ENERGY_CHANGED, self.enemies, self.debug)

        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.energy)

    def test_TalktotheHand(self):
        # Deal 5(7) damage. Whenever you attack this enemy, gain 2(3) {{Block}}. {{Exhaust}}.
        self.new_enemy = copy.deepcopy(self.enemy)

        card = TalktotheHand(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertIn(card, self.player.deck.exhaust_pile)

        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block_gain)

        self.player.block = 0
        self.enemies.append(self.new_enemy)

        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.new_enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

        self.player.energy = 3
        followup = FollowUp(self.player)
        self.player.deck.hand.append(followup)
        self.player.play_card(followup, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.block_gain*followup.attacks)

    def test_Tantrum(self):
        # Deal 3 damage 3(4) times. Enter {{Wrath}}. Shuffle this card into your draw pile.
        card = Tantrum(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (card.damage * card.attacks))
        self.assertIn(card, self.player.deck.draw_pile)
        self.assertNotIn(card, self.player.deck.discard_pile)

    def test_ThirdEye(self):
        # Gain 7(9) {{Block}}. {{Scry}} 3(5).
        card = ThirdEye(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.discard_pile)
        self.assertEqual(self.player.block, card.block)

    def test_Tranquility(self):
        # {{Retain}}. Enter {{Calm}}. {{Exhaust}}.
        card = Tranquility(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.stance, Player.Stance.CALM)
        self.assertIn(card, self.player.deck.exhaust_pile)

        self.player.deck.hand.append(card)
        self.player.end_turn(self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_Vault(self):
        # Take an extra turn after this one. End your turn. {{Exhaust}}.
        self.player.deck.draw_pile.extend([Strike(self.player) for i in range(5)])
        card = Vault(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        self.assertIn(card, self.player.deck.exhaust_pile)
        self.assertEqual(self.player.energy, self.player.max_energy)
        self.assertEqual(len(self.player.deck.hand), 5)

    def test_Vigilance(self):
        # Enter {{Calm}}. Gain 8(12) {{Block}}.
        card = Vigilance(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.stance, Player.Stance.CALM)
        self.assertEqual(self.player.block, card.block)

    def test_Wallop(self):
        # Deal 9(12) damage. Gain {{Block}} equal to unblocked damage dealt.
        card = Wallop(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-card.damage)
        self.assertEqual(self.player.block, card.damage)

        self.player.energy = self.energy

        self.player.block = 0
        enemy_block = 5
        self.enemy.block = enemy_block
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, card.damage - enemy_block)

    def test_WaveoftheHand(self):
        # Whenever you gain {{Block}} this turn, apply 1(2) {{Weak}} to ALL enemies.
        card = WaveoftheHand(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        defend = Defend(self.player)
        self.player.deck.hand.append(defend)
        self.player.play_card(defend, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_dealt_multiplier, 0.75)

    def test_weave(self):
        # Deal 4(6) damage. Whenever you {{Scry}}, return this from the discard pile to your Hand.
        card = Weave(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        ctf = CutThroughFate(self.player)
        self.player.deck.draw_pile.extend(Strike(self.player) for i in range(5))
        self.player.deck.hand.append(ctf)
        self.player.play_card(ctf, self.enemy, self.enemies, self.debug)
        self.assertIn(card, self.player.deck.hand)

    def test_WheelKick(self):
        # Deal 15(20) damage. Draw 2 cards.
        card = WheelKick(self.player)
        self.player.deck.hand.append(card)
        self.player.deck.draw_pile.extend(Strike(self.player) for i in range(5))
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)
        self.assertEqual(len(self.player.deck.hand), card.draw)

    def test_WindmillStrike(self):
        # {{Retain}}. Deal 7(10) damage. Whenever this card is {{Retained}}, increase its damage by 4(5).
        card = WindmillStrike(self.player)
        initial_damage = card.damage
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - card.damage)

        self.player.energy = 3
        self.enemy_start_health = 70
        self.enemy.health = self.enemy_start_health

        self.player.deck.hand.append(card)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.player.notify_listeners(Listener.Event.CARD_RETAINED, self.enemies, self.debug)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (initial_damage + (card.damage_increase * 3)))

    def test_Wish(self):
        # Choose one: Gain 6(8) {{Plated Armor}}, 3(4) {{Strength}}, or 25(30) Gold. {{Exhaust}}.
        seed = 25

        card = Wish(self.player)
        self.player.deck.hand.append(card)
        random.seed(seed)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        random.seed(seed)
        choice = random.randint(0, 2)
        if choice == 0:
            self.assertEqual(self.player.damage_dealt_modifier, card.strength_gain)
        elif choice == 1:
            self.assertEqual(self.player.gold, self.gold + card.gold)
        elif choice == 2:
            self.player.end_turn(self.enemies, self.debug)
            self.assertEqual(self.player.block, card.plated_armor)

    def test_Worship(self):
        # ({{Retain}}.) Gain 5 {{Mantra}}.
        card = Worship(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.mantra, card.mantra)

    def test_WreathOfFlame(self):
        # Your next Attack deals 5(8) additional damage.
        card = WreathofFlame(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)

        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (strike.damage + card.temp_strength_gain)*strike.attacks)

if __name__ == '__main__':
    unittest.main()
