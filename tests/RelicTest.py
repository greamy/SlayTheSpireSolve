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
from CombatSim.Items.Relics.DisplayCase.AncientTeaSet import AncientTeaSet
from CombatSim.Items.Relics.DisplayCase.ArtOfWar import ArtOfWar
from CombatSim.Items.Relics.DisplayCase.BagOfMarbles import BagOfMarbles
from CombatSim.Items.Relics.DisplayCase.BagOfPreparation import BagOfPreparation
from CombatSim.Items.Relics.DisplayCase.BloodVial import BloodVial
from CombatSim.Items.Relics.DisplayCase.BlueCandle import BlueCandle
from CombatSim.Items.Relics.DisplayCase.BottledFlame import BottledFlame
from CombatSim.Items.Relics.DisplayCase.BronzeScales import BronzeScales
from CombatSim.Items.Relics.DisplayCase.CeramicFish import CeramicFish
from CombatSim.Items.Relics.DisplayCase.CentennialPuzzle import CentennialPuzzle
from CombatSim.Items.Relics.DisplayCase.Damaru import Damaru
from CombatSim.Items.Relics.DisplayCase.DreamCatcher import DreamCatcher
from CombatSim.Items.Relics.DisplayCase.HappyFlower import HappyFlower
from CombatSim.Items.Relics.DisplayCase.HolyWater import HolyWater
from CombatSim.Items.Relics.DisplayCase.JuzuBracelet import JuzuBracelet
from CombatSim.Items.Relics.DisplayCase.Lantern import Lantern
from CombatSim.Items.Relics.DisplayCase.MawBank import MawBank
from CombatSim.Items.Relics.DisplayCase.MealTicket import MealTicket
from CombatSim.Items.Relics.DisplayCase.Nunchaku import Nunchaku
from CombatSim.Items.Relics.DisplayCase.OddlySmoothStone import OddlySmoothStone
from CombatSim.Items.Relics.DisplayCase.Omamori import Omamori
from CombatSim.Items.Relics.DisplayCase.Orichalcum import Orichalcum
from CombatSim.Items.Relics.DisplayCase.PenNib import PenNib
from CombatSim.Items.Relics.DisplayCase.PotionBelt import PotionBelt
from CombatSim.Items.Relics.DisplayCase.PreservedInsect import PreservedInsect
from CombatSim.Items.Relics.DisplayCase.RegalPillow import RegalPillow
from CombatSim.Items.Relics.DisplayCase.SmilingMask import SmilingMask
from CombatSim.Items.Relics.DisplayCase.Strawberry import Strawberry
from CombatSim.Items.Relics.DisplayCase.TheBoot import TheBoot
from CombatSim.Items.Relics.DisplayCase.TinyChest import TinyChest
from CombatSim.Items.Relics.DisplayCase.TinyOrnithopter import TinyOrnithopter
from CombatSim.Items.Relics.DisplayCase.Vajra import Vajra
from CombatSim.Items.Relics.DisplayCase.WarPaint import WarPaint
from CombatSim.Items.Relics.DisplayCase.Whetstone import Whetstone
from GameSim.Input.RandomPlayerController import RandomPlayerController


class RelicTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.controller = RandomPlayerController(delay=0)
        self.player = Player(self.health, self.energy, self.gold, [], [], [], self.controller, library_path="CombatSim/Actions/Library")

        self.ascension = 20
        self.act = 1
        self.enemy = JawWorm(self.ascension, self.act)
        self.enemy_start_health = self.enemy.health

        self.enemies = [self.enemy]
        self.debug = False

    def test_holy_water(self):
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
        self.assertEqual(self.enemy.health, self.enemy_start_health - TheBoot.BOOT_DAMAGE)

        # Shouldnt care about the damage dealt modifier
        self.player.deck.hand.append(flurry)
        self.player.damage_dealt_modifier = -2 # give us -2 strength

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

    def test_bag_of_marbles(self):
        # At the start of each combat, apply 1 Vulnerable to ALL enemies.
        relic = BagOfMarbles(self.player)
        self.player.add_relic(relic)

        self.new_enemy = copy.deepcopy(self.enemy)
        self.enemies.append(self.new_enemy)

        self.assertEqual(1.0, self.enemy.damage_taken_multiplier)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(1.5, self.enemy.damage_taken_multiplier)
        self.assertEqual(1.5, self.new_enemy.damage_taken_multiplier)

        self.player.end_turn(self.enemies, self.debug)
        for enemy in self.enemies:
            enemy.start_turn(self.enemies, self.debug)
            enemy.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        for enemy in self.enemies:
            self.assertEqual(enemy.damage_taken_multiplier, 1.0)

    def test_bag_of_preparation(self):
        # At the start of each combat, draw 2 additional cards.
        relic = BagOfPreparation(self.player)
        self.player.add_relic(relic)

        self.player.deck.draw_pile = [Strike(self.player) for _ in range(10)]
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount + BagOfPreparation.DRAW_AMT)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount)

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

    def test_centennial_puzzle(self):
        # The first time you lose HP each combat, draw 3 cards.
        relic = CentennialPuzzle(self.player)
        self.player.add_relic(relic)

        self.player.deck.draw_pile = [Strike(self.player) for _ in range(10)]
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(len(self.player.deck.hand), self.player.draw_amount)

        self.enemy.intent = self.enemy.intent_set[JawWorm.CHOMP]
        self.enemy.do_turn(self.player, self.debug)
        self.assertEqual(self.player.draw_amount + CentennialPuzzle.DRAW_AMT, len(self.player.deck.hand))

        self.enemy.intent = self.enemy.intent_set[JawWorm.CHOMP]
        self.enemy.do_turn(self.player, self.debug)
        self.assertEqual(self.player.draw_amount + CentennialPuzzle.DRAW_AMT, len(self.player.deck.hand))

    def test_happy_flower(self):
        # Every 3 turns, gain 1 Energy.
        relic = HappyFlower(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy)

        for i in range(2):
            self.player.start_turn(self.enemies, self.debug)
            self.assertEqual(self.player.max_energy, self.player.energy)
            self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual( self.player.max_energy + 1, self.player.energy)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.max_energy, self.player.energy)

    def test_bronze_scales(self):
        # Start each combat with 3 Thorns.
        relic = BronzeScales(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.enemy.intent = self.enemy.intent_set[JawWorm.CHOMP] # player takes damage
        self.enemy.do_turn(self.player, self.debug)
        self.assertEqual(self.enemy_start_health - BronzeScales.THORNS_AMOUNT, self.enemy.health) # check thorns dmg

        self.enemy.intent = self.enemy.intent_set[JawWorm.BELLOW] # player won't take damage
        self.enemy.do_turn(self.player, self.debug)
        self.assertEqual(self.enemy_start_health - BronzeScales.THORNS_AMOUNT, self.enemy.health) # check thorns didn't trigger again

    def test_ceramic_fish(self):
        # Whenever you add a card to your deck, gain 9 gold.
        relic = CeramicFish(self.player)
        self.player.add_relic(relic)

        start_gold = self.player.gold
        self.player.add_card("Strike")
        self.assertEqual(self.player.gold, start_gold + CeramicFish.GOLD_AMOUNT)

    def test_dream_catcher(self):
        # Whenever you rest, you may add a card to your deck.
        relic = DreamCatcher(self.player)
        self.player.add_relic(relic)

        num_in_deck = len(self.player.deck.draw_pile)
        self.player.do_rest()
        self.assertEqual(len(self.player.deck.draw_pile), num_in_deck + 1)

    def test_ancient_tea_set(self):
        # Whenever you enter a Rest Site, start the next combat with 2 extra Energy.
        relic = AncientTeaSet(self.player)
        self.player.add_relic(relic)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy)
        # self.player.end_combat(self.enemies, self.debug)

        self.player.do_rest()
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy + AncientTeaSet.ENERGY_AMOUNT)

    @unittest.skip("TODO: Implement ? rooms")
    def test_juzu_bracelet(self):
        # Regular enemy combats are no longer encountered in ? rooms.
        relic = JuzuBracelet(self.player)
        self.player.add_relic(relic)

        #TODO: Implement ? rooms!!!

    def test_Lantern(self):
        # Gain 1 energy on the first turn of each combat
        relic = Lantern(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy + 1)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy)

    @unittest.skip("TODO: Implement shop and gold spending")
    def test_maw_bank(self):
        # Whenever you climb a floor, gain 12 Gold. No longer works when you spend any Gold at the shop.
        relic = MawBank(self.player)
        self.player.add_relic(relic)

        start_gold = self.player.gold
        self.player.climb_floor()
        self.assertEqual(self.player.gold, start_gold + MawBank.GOLD_AMT)

        self.player.shop()
        self.assertEqual(relic.active, False)

    def test_meal_ticket(self):
        # Whenever you enter a shop room, heal 15 HP.
        relic = MealTicket(self.player)
        self.player.add_relic(relic)

        self.player.health -= 20
        start_health = self.player.health
        self.player.shop()
        self.assertEqual(start_health + MealTicket.HEAL_AMOUNT, self.player.health)

        self.player.shop()
        self.assertEqual(relic.active, False)

    def test_nunchaku(self):
        # Whenever you play 10 Attacks in a single turn, gain 1 energy
        relic = Nunchaku(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(10):
            self.player.add_card("FlurryofBlows")

        self.player.start_turn(self.enemies, self.debug)
        for i in range(self.player.draw_amount):
            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.player.max_energy, self.player.energy)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        for i in range(self.player.draw_amount):
            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

        self.assertEqual(self.player.max_energy + 1, self.player.energy)

    def test_oddly_smooth_stone(self):
        # At the start of each combat, gain 1 Dexterity.
        relic = OddlySmoothStone(self.player)
        self.player.add_relic(relic)

        self.player.deck.draw_pile = [Defend(self.player) for _ in range(10)]
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.block_modifier, OddlySmoothStone.DEXTERITY_AMOUNT)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(5 + OddlySmoothStone.DEXTERITY_AMOUNT, self.player.block)

    def test_Omamori(self):
        # Negate the next 2 Curses you obtain.
        relic = Omamori(self.player)
        self.player.add_relic(relic)

        self.player.add_card("CurseoftheBell")
        self.assertEqual(len(self.player.deck.draw_pile), 0)

    def test_pen_nib(self):
        # Whenever you play 10 Attacks in a single turn, gain 1 energy
        relic = PenNib(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(10):
            self.player.add_card("FlurryofBlows")

        self.player.start_turn(self.enemies, self.debug)
        for i in range(self.player.draw_amount):
            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.player.max_energy, self.player.energy)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        for i in range(self.player.draw_amount-1):
            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

        enemy_cur_health = self.enemy.health
        card_to_play = self.player.deck.hand[0]
        self.player.play_card(card_to_play, self.enemy, self.enemies, self.debug)

        self.assertEqual(enemy_cur_health - (card_to_play.damage * 2), self.enemy.health)

    @unittest.skip("TODO: Implement potions")
    def test_potion_belt(self):
        # Upon pick up, gain 2 potion slots.
        relic = PotionBelt(self.player)
        self.player.add_relic(relic)

    @unittest.skip("TODO: Trigger listeners when enter elite room")
    def test_preserved_insect(self):
        # Enemies in Elite rooms have 25% less HP.
        relic = PreservedInsect(self.player)
        self.player.add_relic(relic)

    def test_regal_pillow(self):
        # Heal an additional 15 HP when you Rest.
        relic = RegalPillow(self.player)
        self.player.add_relic(relic)

        self.player.health = 10
        start_hp = 10
        amt = self.player.do_rest()
        self.assertEqual(self.player.health, start_hp + amt + RegalPillow.HEAL_AMOUNT)

    @unittest.skip("TODO: Implement shop and gold spending")
    def test_smiling_mask(self):
        # The merchant's card removal service now always costs 50 Gold.
        relic = SmilingMask(self.player)
        self.player.add_relic(relic)

    def test_strawberry(self):
        # Upon pickup, raise your Max HP by 7.
        relic = Strawberry(self.player)
        self.player.add_relic(relic)

        self.assertEqual(self.player.start_health, self.health + Strawberry.MAX_HP_AMOUNT)
        self.assertEqual(self.player.health, self.health + Strawberry.MAX_HP_AMOUNT)

    @unittest.skip("TODO: Implement ? rooms")
    def test_tiny_chest(self):
        # Every 4th ? room is a Treasure room.
        relic = TinyChest(self.player)
        self.player.add_relic(relic)

        # TODO: Implement ? rooms!!!

    @unittest.skip("TODO: Implement Potions!")
    def test_tiny_ornithopter(self):
        # Whenever you use a potion, heal 5 HP.
        relic = TinyOrnithopter(self.player)
        self.player.add_relic(relic)

        # TODO: Implement potions

    def test_vajra(self):
        # At the start of each combat, gain 1 Strength.
        relic = Vajra(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.damage_dealt_modifier, Vajra.STRENGTH_AMOUNT)

    def test_war_paint(self):
        # Upon pick up, Upgrade 2 random Skills.
        relic = WarPaint(self.player)

        self.player.add_card("Defend")
        self.player.add_card("Defend")

        self.player.add_relic(relic)

        self.assertEqual(self.player.deck.draw_pile[0].upgraded, True)
        self.assertEqual(self.player.deck.draw_pile[1].upgraded, True)

        self.player.deck.draw_pile.clear()
        self.assertEqual(len(self.player.deck), 0)

        self.player.add_card("Defend")
        self.player.add_card("Defend")
        self.player.add_card("Defend")

        self.player.add_relic(relic)
        un_upgraded_cards = [card for card in self.player.deck if not card.upgraded]
        self.assertEqual(len(un_upgraded_cards), 1)

    def test_whetstone(self):
        # Upon pick up, Upgrade 2 random Skills.
        relic = Whetstone(self.player)

        self.player.add_card("Strike")
        self.player.add_card("Strike")

        self.player.add_relic(relic)

        self.assertEqual(self.player.deck.draw_pile[0].upgraded, True)
        self.assertEqual(self.player.deck.draw_pile[1].upgraded, True)

        self.player.deck.draw_pile.clear()
        self.assertEqual(len(self.player.deck), 0)

        self.player.add_card("Strike")
        self.player.add_card("Strike")
        self.player.add_card("Strike")

        self.player.add_relic(relic)
        un_upgraded_cards = [card for card in self.player.deck if not card.upgraded]
        self.assertEqual(len(un_upgraded_cards), 1)

    def test_damaru(self):
        # At the start of your turn, gain 1 Mantra.
        relic = Damaru(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.mantra, 1)

    def test_blue_candle(self):
        # Curse cards can now be played. Playing a Curse will make you lose 1 HP and Exhausts the card.
        curse_card = self.player.add_card("CurseoftheBell")

        relic = BlueCandle(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        curse_success = self.player.play_card(curse_card, self.enemy, self.enemies, self.debug)
        self.assertEqual(True, curse_success)
        self.assertEqual(self.player.health, self.health - 1)

    def test_bottled_flame(self):
        # Upon pick up, choose an Attack. Start each combat with this card in your hand.

        # TODO: Make sure this only chooses attacks
        strike = self.player.add_card("Strike")

        relic = BottledFlame(self.player)
        self.player.add_relic(relic)

        self.assertTrue(strike.innate)

        for i in range(10):
            self.player.add_card("Defend")
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(strike, self.player.deck.hand)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(strike, self.player.deck.hand)
