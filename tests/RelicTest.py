import unittest
import copy

from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.FlurryofBlows import FlurryofBlows
from CombatSim.Actions.Library.FlyingSleeves import FlyingSleeves
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.Akabeko import Akabeko
from CombatSim.Items.Relics.DisplayCase.Anchor import Anchor
from CombatSim.Items.Relics.DisplayCase.ArtOfWar import ArtOfWar
from CombatSim.Items.Relics.DisplayCase.BagOfMarbles import BagOfMarbles
from CombatSim.Items.Relics.DisplayCase.BagOfPreparation import BagOfPreparation
from CombatSim.Items.Relics.DisplayCase.BloodVial import BloodVial
from CombatSim.Items.Relics.DisplayCase.CentennialPuzzle import CentennialPuzzle
from CombatSim.Items.Relics.DisplayCase.HappyFlower import HappyFlower
from CombatSim.Items.Relics.DisplayCase.HolyWater import HolyWater
from CombatSim.Items.Relics.DisplayCase.Orichalcum import Orichalcum
from CombatSim.Items.Relics.DisplayCase.TheBoot import TheBoot


class RelicTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.player = Player(self.health, self.energy, self.gold, [], [], [], library_path="../CombatSim/Actions/Library")

        self.ascension = 20
        self.act = 1
        self.enemy = JawWorm(self.ascension, self.act)
        self.enemy_start_health = self.enemy.health

        self.enemies = [self.enemy]
        self.debug = False

    def test_holy_water(self):
        # ({{Innate}}.) Shuffle a {{C|Beta}} into your draw pile. {{Exhaust}}.
        relic = HolyWater(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 1)

        self.player.deck.hand.clear()

        self.player.drop_relic(relic)
        self.assertEqual(len(self.player.relics), 0)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), 0)

    def test_anchor(self):
        relic = Anchor(self.player)
        self.player.add_relic(relic)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.block, 10)
        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)
        self.player.end_turn(self.enemies, self.debug)

        self.player.drop_relic(relic)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)


    def test_orichalcum(self):
        card = Defend(self.player)
        relic = Orichalcum(self.player)
        self.player.add_relic(relic)
        self.player.end_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, 6)

        self.player.start_turn(self.enemies, self.debug)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)
        self.assertEqual(card.block, self.player.block)


    def test_akabeko(self):
        # Your first attack each combat deals 8 additional damage.
        relic = Akabeko(self.player)
        card = Strike(self.player)
        self.player.add_relic(relic)
        self.player.start_turn(self.enemies, self.debug)
        self.player.deck.hand.append(card)
        self.player.play_card(card,self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(card.damage+8))
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health,self.enemy_start_health-(card.damage+8)-card.damage)


    def test_boot(self):
        # Whenever you would deal 4 or less unblocked Attack damage, increase it to 5.
        relic = TheBoot(self.player)
        flurry = FlurryofBlows(self.player)

        self.player.add_relic(relic)
        self.player.begin_combat(self.enemies, self.debug)
        self.player.deck.hand.append(flurry)

        self.player.play_card(flurry, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 5)

        # Shouldnt care about the damage dealt modifier
        self.player.deck.hand.append(flurry)
        self.player.damage_dealt_modifier = -2

        self.player.play_card(flurry, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 10)

        # Shouldn't apply to 0 damage attacks
        self.player.deck.hand.append(flurry)
        self.player.damage_dealt_modifier = -4

        self.player.play_card(flurry, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - 10)

        # Check attacks with multiple attacks, and multiple enemies
        self.setUp()
        relic = TheBoot(self.player)
        sleeves = FlyingSleeves(self.player)
        self.new_enemy = copy.deepcopy(self.enemy)
        self.enemies.append(self.new_enemy)

        self.player.add_relic(relic)
        self.player.begin_combat(self.enemies, self.debug)
        self.player.deck.hand.append(sleeves)

        self.player.play_card(sleeves, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - (5*sleeves.attacks))

        self.enemy.health = self.enemy_start_health
        # reset boot enemy health tracking by starting a new turn
        self.player.start_turn(self.enemies, self.debug)

        # Ensure attacks with big damage don't get modified
        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health - strike.damage)

    @unittest.skip("art of war not implemented")
    def test_art_of_war(self):
        # If you do not play any Attacks during your turn, gain an extra Energy next turn.
        relic = ArtOfWar(self.player)
        card = Defend(self.player)

        self.player.add_relic(relic)
        self.player.start_turn(self.enemies, self.debug)
        # Full turn of defends gives energy next turn
        self.player.deck.hand.append(card)
        self.player.deck.hand.append(card)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy + 1)

        # Playing an attack should not give energy next turn
        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy)

    @unittest.skip("bag of marbles not implemented")
    def test_bag_of_marbles(self):
        # At the start of each combat, apply 1 Vulnerable to ALL enemies.
        relic = BagOfMarbles(self.player)
        self.player.add_relic(relic)

        self.new_enemy = copy.deepcopy(self.enemy)
        self.enemies.append(self.new_enemy)

        self.assertEqual(self.enemy.damage_taken_multiplier, 1)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.enemy.damage_taken_multiplier, 1.5)
        self.assertEqual(self.new_enemy.damage_taken_multiplier, 1.5)

        self.player.end_turn(self.enemies, self.debug)
        for enemy in self.enemies:
            enemy.start_turn(self.enemies, self.debug)
            enemy.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        for enemy in self.enemies:
            self.assertEqual(enemy.damage_taken_multiplier, 1.0)

    @unittest.skip("bag of preparation not implemented")
    def test_bag_of_preparation(self):
        # At the start of each combat, draw 2 additional cards.
        relic = BagOfPreparation(self.player)
        self.player.add_relic(relic)

        self.player.deck.draw_pile = [Strike(self.player) for _ in range(10)]
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount + 2)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount)

    @unittest.skip("blood vial not implemented")
    def test_blood_vial(self):
        # At the start of each combat, heal 2 HP.
        relic = BloodVial(self.player)
        self.player.add_relic(relic)
        start_hp = 50
        self.player.health = start_hp

        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.health, start_hp + 2)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.health, start_hp + 2)

    @unittest.skip("centennial puzzle not implemented")
    def test_centennial_puzzle(self):
        # The first time you lose HP each combat, draw 3 cards.
        relic = CentennialPuzzle(self.player)
        self.player.add_relic(relic)

        self.player.deck.draw_pile = [Strike(self.player) for _ in range(10)]
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount)

        self.player.take_damage(10)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount + 3)

        self.player.take_damage(10)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount + 3)

    @unittest.skip("happy flower not implemented")
    def test_happy_flower(self):
        # Every 3 turns, gain 1 Energy.
        relic = HappyFlower(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy)

        for i in range(2):
            self.player.start_turn(self.enemies, self.debug)
            self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy + 1)

