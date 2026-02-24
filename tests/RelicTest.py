import unittest
import copy

from CombatSim.Actions.Card import Card
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
from CombatSim.Items.Relics.DisplayCase.BottledLightning import BottledLightning
from CombatSim.Items.Relics.DisplayCase.BottledTornado import BottledTornado
from CombatSim.Items.Relics.DisplayCase.BronzeScales import BronzeScales
from CombatSim.Items.Relics.DisplayCase.CeramicFish import CeramicFish
from CombatSim.Items.Relics.DisplayCase.CentennialPuzzle import CentennialPuzzle
from CombatSim.Items.Relics.DisplayCase.Damaru import Damaru
from CombatSim.Items.Relics.DisplayCase.DarkstonePeriapt import DarkstonePeriapt
from CombatSim.Items.Relics.DisplayCase.DreamCatcher import DreamCatcher
from CombatSim.Items.Relics.DisplayCase.EternalFeather import EternalFeather
from CombatSim.Items.Relics.DisplayCase.FrozenEgg import FrozenEgg
from CombatSim.Items.Relics.DisplayCase.GremlinHorn import GremlinHorn
from CombatSim.Items.Relics.DisplayCase.HappyFlower import HappyFlower
from CombatSim.Items.Relics.DisplayCase.HolyWater import HolyWater
from CombatSim.Items.Relics.DisplayCase.HornCleat import HornCleat
from CombatSim.Items.Relics.DisplayCase.InkBottle import InkBottle
from CombatSim.Items.Relics.DisplayCase.JuzuBracelet import JuzuBracelet
from CombatSim.Items.Relics.DisplayCase.Kunai import Kunai
from CombatSim.Items.Relics.DisplayCase.Lantern import Lantern
from CombatSim.Items.Relics.DisplayCase.LetterOpener import LetterOpener
from CombatSim.Items.Relics.DisplayCase.Matryoshka import Matryoshka
from CombatSim.Items.Relics.DisplayCase.MawBank import MawBank
from CombatSim.Items.Relics.DisplayCase.MealTicket import MealTicket
from CombatSim.Items.Relics.DisplayCase.MeatOnTheBone import MeatOnTheBone
from CombatSim.Items.Relics.DisplayCase.MercuryHourglass import MercuryHourglass
from CombatSim.Items.Relics.DisplayCase.MoltenEgg import MoltenEgg
from CombatSim.Items.Relics.DisplayCase.MummifiedHand import MummifiedHand
from CombatSim.Items.Relics.DisplayCase.Nunchaku import Nunchaku
from CombatSim.Items.Relics.DisplayCase.OddlySmoothStone import OddlySmoothStone
from CombatSim.Items.Relics.DisplayCase.Omamori import Omamori
from CombatSim.Items.Relics.DisplayCase.Orichalcum import Orichalcum
from CombatSim.Items.Relics.DisplayCase.OrnamentalFan import OrnamentalFan
from CombatSim.Items.Relics.DisplayCase.Pantograph import Pantograph
from CombatSim.Items.Relics.DisplayCase.Pear import Pear
from CombatSim.Items.Relics.DisplayCase.PenNib import PenNib
from CombatSim.Items.Relics.DisplayCase.PotionBelt import PotionBelt
from CombatSim.Items.Relics.DisplayCase.PreservedInsect import PreservedInsect
from CombatSim.Items.Relics.DisplayCase.QuestionCard import QuestionCard
from CombatSim.Items.Relics.DisplayCase.RegalPillow import RegalPillow
from CombatSim.Items.Relics.DisplayCase.Shuriken import Shuriken
from CombatSim.Items.Relics.DisplayCase.SingingBowl import SingingBowl
from CombatSim.Items.Relics.DisplayCase.SmilingMask import SmilingMask
from CombatSim.Items.Relics.DisplayCase.Strawberry import Strawberry
from CombatSim.Items.Relics.DisplayCase.StrikeDummy import StrikeDummy
from CombatSim.Items.Relics.DisplayCase.Sundial import Sundial
from CombatSim.Items.Relics.DisplayCase.TheBoot import TheBoot
from CombatSim.Items.Relics.DisplayCase.TheCourier import TheCourier
from CombatSim.Items.Relics.DisplayCase.TinyChest import TinyChest
from CombatSim.Items.Relics.DisplayCase.TinyOrnithopter import TinyOrnithopter
from CombatSim.Items.Relics.DisplayCase.ToxicEgg import ToxicEgg
from CombatSim.Items.Relics.DisplayCase.Vajra import Vajra
from CombatSim.Items.Relics.DisplayCase.WarPaint import WarPaint
from CombatSim.Items.Relics.DisplayCase.Whetstone import Whetstone
from CombatSim.Items.Relics.DisplayCase.WhiteBeastStatue import WhiteBestStatue
from GameSim.Input.RandomPlayerController import RandomPlayerController


class RelicTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        self.controller = RandomPlayerController(delay=0)
        self.lib_path = "../CombatSim/Actions/Library"
        self.player = Player(self.health, self.energy, self.gold, [], [], [], self.controller, library_path=self.lib_path)

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
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.draw_amount + CentennialPuzzle.DRAW_AMT, len(self.player.deck.hand))

        self.enemy.intent = self.enemy.intent_set[JawWorm.CHOMP]
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
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
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.enemy_start_health - BronzeScales.THORNS_AMOUNT, self.enemy.health) # check thorns dmg

        self.enemy.intent = self.enemy.intent_set[JawWorm.BELLOW] # player won't take damage
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
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

    def test_pear(self):
        relic = Pear(self.player)
        self.player.add_relic(relic)

        self.assertEqual(self.player.start_health, self.health + Pear.MAX_HP_AMOUNT)
        self.assertEqual(self.player.health, self.health + Pear.MAX_HP_AMOUNT)

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
        strike = self.player.add_card("Strike")
        for i in range(10):
            self.player.add_card("Defend")

        relic = BottledFlame(self.player)
        self.player.add_relic(relic)

        self.assertTrue(strike.innate)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(strike, self.player.deck.hand)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(strike, self.player.deck.hand)

    def test_bottled_lightning(self):
        # Upon pick up, choose a Skill. Start each combat with this card in your hand.
        defend = self.player.add_card("Defend")
        for i in range(10):
            self.player.add_card("Strike")

        relic = BottledLightning(self.player)
        self.player.add_relic(relic)

        self.assertTrue(defend.innate)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(defend, self.player.deck.hand)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(defend, self.player.deck.hand)

    def test_bottled_tornado(self):
        # Upon pick up, choose a Power. Start each combat with this card in your hand.
        rushdown = self.player.add_card("Rushdown")
        for i in range(10):
            self.player.add_card("Strike")

        relic = BottledTornado(self.player)
        self.player.add_relic(relic)

        self.assertTrue(rushdown.innate)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(rushdown, self.player.deck.hand)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertIn(rushdown, self.player.deck.hand)

    def test_bottles_no_target(self):
        relic = BottledTornado(self.player)
        self.player.add_relic(relic)

        relic2 = BottledLightning(self.player)
        self.player.add_relic(relic2)

        relic3 = BottledFlame(self.player)
        self.player.add_relic(relic3)

    def test_darkstone_periapt(self):
        # Whenever you obtain a Curse, increase your Max HP by 6.
        relic = DarkstonePeriapt(self.player)
        self.player.add_relic(relic)

        self.player.add_card("CurseoftheBell")
        self.assertEqual(self.player.start_health, self.health + DarkstonePeriapt.MAX_HP_GAIN)

    def test_eternal_feather(self):
        # For every 5 cards in your deck, heal 3 HP whenever you enter a Rest Site.
        relic = EternalFeather(self.player)
        self.player.add_relic(relic)

        for i in range(EternalFeather.NUM_CARDS_PER_SET):
            self.player.add_card("Strike")

        self.player.health = 10
        start_hp = 10
        self.player.enter_rest()
        self.assertEqual(self.player.health, start_hp + EternalFeather.HEAL_PER_CARD_SET)

        for i in range(EternalFeather.NUM_CARDS_PER_SET):
            self.player.add_card("Defend")

        self.player.health = 10
        start_hp = 10
        self.player.enter_rest()
        self.assertEqual(self.player.health, start_hp + 2*EternalFeather.HEAL_PER_CARD_SET)

    def test_frozen_egg(self):
        # Whenever you add a Power card to your deck, it is Upgraded.
        battlehymn = self.player.add_card("BattleHymn") #added before the relic, should never be upgraded.
        self.assertFalse(battlehymn.upgraded)

        relic = FrozenEgg(self.player)
        self.player.add_relic(relic)

        rushdown = self.player.add_card("Rushdown")
        self.assertTrue(rushdown.upgraded)
        self.assertFalse(battlehymn.upgraded)

        for i in range(2):
            strike = self.player.add_card("Strike")
            self.assertFalse(strike.upgraded)
        for j in range(2):
            defend = self.player.add_card("Defend")
            self.assertFalse(defend.upgraded)

        rushdown_copy2 = self.player.add_card("Rushdown")
        self.assertTrue(rushdown_copy2.upgraded)

        battlehymn_copy2 = self.player.add_card("BattleHymn")
        self.assertTrue(battlehymn_copy2.upgraded)

        self.assertFalse(battlehymn.upgraded)

    def test_molten_egg(self):
        # Whenever you add an Attack card to your deck, it is Upgraded.
        bowlingbash = self.player.add_card("BowlingBash") #added before the relic, should never be upgraded.
        self.assertFalse(bowlingbash.upgraded)

        relic = MoltenEgg(self.player)
        self.player.add_relic(relic)

        strike = self.player.add_card("Strike")
        self.assertTrue(strike.upgraded)
        self.assertFalse(bowlingbash.upgraded)

        for i in range(2):
            strike = self.player.add_card("Rushdown")
            self.assertFalse(strike.upgraded)
        for j in range(2):
            defend = self.player.add_card("Defend")
            self.assertFalse(defend.upgraded)

        strike_copy2 = self.player.add_card("Strike")
        self.assertTrue(strike_copy2.upgraded)

        bowlingbash_copy2 = self.player.add_card("BowlingBash")
        self.assertTrue(bowlingbash_copy2.upgraded)

        self.assertFalse(bowlingbash.upgraded)

    def test_toxic_egg(self):
        # Whenever you add a Skill card to your deck, it is Upgraded.
        prostrate = self.player.add_card("Prostrate")  # added before the relic, should never be upgraded.
        self.assertFalse(prostrate.upgraded)

        relic = ToxicEgg(self.player)
        self.player.add_relic(relic)

        defend = self.player.add_card("Defend")
        self.assertTrue(defend.upgraded)
        self.assertFalse(prostrate.upgraded)

        for i in range(2):
            strike = self.player.add_card("Rushdown")
            self.assertFalse(strike.upgraded)
        for j in range(2):
            defend = self.player.add_card("Strike")
            self.assertFalse(defend.upgraded)

        defend_copy2 = self.player.add_card("Defend")
        self.assertTrue(defend_copy2.upgraded)

        prostrate_copy2 = self.player.add_card("Prostrate")
        self.assertTrue(prostrate_copy2.upgraded)

        self.assertFalse(prostrate.upgraded)

    def test_gremlin_horn(self):
        # Whenever an enemy dies, gain 1 Energy and draw 1 card.
        relic = GremlinHorn(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 10
        self.enemy_start_health = 10

        strike1: Card = self.player.add_card("Strike")
        strike2 = self.player.add_card("Strike")
        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)

        self.player.play_card(strike1, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy - strike1.energy)

        self.player.play_card(strike2, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.energy, self.player.max_energy - strike1.energy)
        self.assertIn(strike1, self.player.deck.hand)

    def test_horn_cleat(self):
        # At the start of your 2nd turn, gain 14 Block.
        relic = HornCleat(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, HornCleat.BLOCK_GAIN)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

        self.player.end_combat(self.enemies, self.debug, False)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.assertEqual(self.player.block, HornCleat.BLOCK_GAIN)

    def test_ink_bottle(self):
        # Whenever you play 10 cards, draw 1 card
        relic = InkBottle(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(10):
            self.player.add_card("FlurryofBlows")
        for j in range(2): # ensure it can count up, reset, then do it again.
            self.player.start_turn(self.enemies, self.debug)
            for i in range(self.player.draw_amount):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
                self.assertEqual(self.player.max_energy, self.player.energy)

            self.player.end_turn(self.enemies, self.debug)
            self.player.start_turn(self.enemies, self.debug)
            for i in range(self.player.draw_amount):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

            # still have a card in hand after playing all 5 cards.
            self.assertEqual(len(self.player.deck.hand), 1)
            self.player.end_turn(self.enemies, self.debug)

    def test_kunai(self):
        # Every time you play 3 Attacks in a single turn, gain 1 Dexterity.
        relic = Kunai(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(3):
            self.player.add_card("FlurryofBlows")

        for j in range(2):
            self.player.start_turn(self.enemies, self.debug)
            for i in range(2):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.player.block_modifier, j+1)
            self.player.end_turn(self.enemies, self.debug)

        self.player.block_modifier = 0

        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block_modifier, 0)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block_modifier, 0)

    def test_ornamental_fan(self):
        # Every time you play 3 Attacks in a single turn, gain 4 block.
        relic = OrnamentalFan(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(5):
            self.player.add_card("FlurryofBlows")

        for j in range(2):
            self.player.start_turn(self.enemies, self.debug)
            for i in range(2):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.player.block, OrnamentalFan.BLOCK_AMOUNT)
            self.player.end_turn(self.enemies, self.debug)

        self.player.block = 0

        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.block, 0)

    def test_shuriken(self):
        # Every time you play 3 Attacks in a single turn, gain 1 strength.
        relic = Shuriken(self.player)
        self.player.add_relic(relic)

        self.enemy.health = 1000
        self.enemy_start_health = 1000

        for i in range(3):
            self.player.add_card("FlurryofBlows")

        for j in range(2):
            self.player.start_turn(self.enemies, self.debug)
            for i in range(2):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.player.damage_dealt_modifier, j + 1)
            self.player.end_turn(self.enemies, self.debug)

        self.player.damage_dealt_modifier = 0

        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.damage_dealt_modifier, 0)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.player.damage_dealt_modifier, 0)

    def test_letter_opener(self):
        # Every time you play 3 Skills in a single turn, deal 5 damage to ALL enemies.
        relic = LetterOpener(self.player)
        self.player.add_relic(relic)

        for i in range(3):
            self.player.add_card("Halt")

        for j in range(2):
            self.player.start_turn(self.enemies, self.debug)
            for i in range(2):
                self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)

            self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
            self.assertEqual(self.enemy.start_health - (LetterOpener.DAMAGE_AMOUNT*(j+1)), self.enemy.health)
            self.player.end_turn(self.enemies, self.debug)

        self.enemy.health = self.enemy_start_health

        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.start_health, self.enemy.health)

        self.player.end_turn(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(self.player.deck.hand[0], self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.start_health, self.enemy.health)

    @unittest.skip("TODO: Implement chests")
    def test_matryoshka(self):
        # The next 2 chests you open contain 2 Relics. (Excludes boss chests)
        relic = Matryoshka(self.player)
        self.player.add_relic(relic)

    def test_meat_on_the_bone(self):
        # If your HP is at or below 50% at the end of combat, heal 12 HP.
        relic = MeatOnTheBone(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        damage_taken = 10
        self.player.take_damage(damage_taken)
        self.player.end_combat(self.enemies, self.debug)

        self.assertEqual(self.player.start_health-damage_taken, self.player.health)

        self.player.begin_combat(self.enemies, self.debug)
        new_damage = self.player.start_health//2
        damage_taken = new_damage + damage_taken
        self.player.take_damage(new_damage)
        self.player.end_combat(self.enemies, self.debug)

        self.assertEqual(self.player.start_health - damage_taken + MeatOnTheBone.HEAL_AMOUNT, self.player.health)


    def test_mercury_hourglass(self):
        # At the start of your turn, deal 3 damage to ALL enemies.
        relic = MercuryHourglass(self.player)
        self.player.add_relic(relic)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)

        self.assertEqual(self.enemy.start_health - MercuryHourglass.DAMAGE_AMOUNT, self.enemy.health)
        self.player.end_turn(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)

        self.assertEqual(self.enemy.start_health - (MercuryHourglass.DAMAGE_AMOUNT*2), self.enemy.health)

    def test_mummified_hand(self):
        for i in range(10):
        # Whenever you play a Power, a random card in your hand costs 0 for the turn.
            relic = MummifiedHand(self.player)
            self.player.add_relic(relic)

            rushdown = self.player.add_card("Rushdown")
            strike = self.player.add_card("Strike")
            defend = self.player.add_card("Defend")
            battle_hymn = self.player.add_card("BattleHymn")

            self.player.begin_combat(self.enemies, self.debug)
            self.player.start_turn(self.enemies, self.debug)
            self.player.play_card(rushdown, self.enemy, self.enemies, self.debug)
            self.assertTrue(strike.energy == 0 or defend.energy == 0 or battle_hymn.energy == 0)
            self.player.end_turn(self.enemies, self.debug)
            self.assertFalse(strike.energy == 0 or defend.energy == 0 or battle_hymn.energy == 0)

            rushdown2 = self.player.add_card("Rushdown")

            self.player.start_turn(self.enemies, self.debug)
            self.player.play_card(rushdown2, self.enemy, self.enemies, self.debug)
            self.assertTrue(strike.energy == 0 or defend.energy == 0 or battle_hymn.energy == 0)

            self.player.play_card(battle_hymn, self.enemy, self.enemies, self.debug)
            self.assertTrue(
                (strike.energy == 0 and defend.energy == 0) or
                (strike.energy == 0 and battle_hymn.energy == 0) or
                (defend.energy == 0 and battle_hymn.energy == 0)
            )
            self.setUp()

    def test_Pantograph(self):
        # At the start of boss combats, heal 25 HP.
        relic = Pantograph(self.player)
        self.player.add_relic(relic)

        self.player.health = 10
        self.health = 10

        self.player.begin_combat(self.enemies, self.debug, boss=True)
        self.assertEqual(self.player.health, self.health + Pantograph.HEAL_AMOUNT)

        self.player.health = self.health

        self.player.end_combat(self.enemies, self.debug)
        self.player.begin_combat(self.enemies, self.debug)
        self.assertEqual(self.player.health, self.health)

    @unittest.skip("TODO: Implement Card Rewards")
    def test_question_card(self):
        # On future Card Reward screens you have 1 additional card to choose from.
        relic = QuestionCard(self.player)
        self.player.add_relic(relic)

    @unittest.skip("TODO: Implement Card Rewards")
    def test_singing_bowl(self):
        # When adding cards to your deck, you may gain +2 Max HP instead.
        relic = SingingBowl(self.player)
        self.player.add_relic(relic)

    def test_strike_dummy(self):
        # Cards containing "Strike" deal 3 additional damage.
        relic = StrikeDummy(self.player)
        self.player.add_relic(relic)

        strike = self.player.add_card("Strike")
        self.assertEqual(strike.damage, 6 + StrikeDummy.DAMAGE_INCREASE)

        strike2 = self.player.add_card("Strike")
        self.assertEqual(strike2.damage, 6 + StrikeDummy.DAMAGE_INCREASE)
        self.assertEqual(strike.damage, 6 + StrikeDummy.DAMAGE_INCREASE)

        self.player.begin_combat(self.enemies, self.debug)
        self.player.start_turn(self.enemies, self.debug)
        self.player.play_card(strike, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.start_health - strike.damage, self.enemy.health)

        followup = self.player.add_card("FollowUp")
        self.assertEqual(followup.damage, 7) # unchanged
        self.assertEqual(strike2.damage, 6 + StrikeDummy.DAMAGE_INCREASE) # increased only once
        self.assertEqual(strike.damage, 6 + StrikeDummy.DAMAGE_INCREASE) # increased only once

    def test_sundial(self):
        # Every 3 times you shuffle your draw pile, gain 2 Energy.
        relic = Sundial(self.player)
        self.player.add_relic(relic)

        self.player.add_card("Strike")
        self.player.add_card("Defend")

        # shuffle 1 and 2 times make sure energy stays the same
        self.player.begin_combat(self.enemies, self.debug)

        self.player.start_turn(self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)
        self.player.shuffle_discard(self.enemies, self.debug)
        self.assertEqual(self.energy, self.player.energy)

        self.player.start_turn(self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)
        self.player.shuffle_discard(self.enemies, self.debug)
        self.assertEqual(self.energy, self.player.energy)

        # then shuffle third time and check energy increased.
        self.player.start_turn(self.enemies, self.debug)
        self.player.end_turn(self.enemies, self.debug)
        self.player.shuffle_discard(self.enemies, self.debug)
        self.assertEqual(self.energy + Sundial.ENERGY_AMOUNT, self.player.energy)

        self.player.energy = self.energy

    @unittest.skip("TODO: Implement combat rewards")
    def test_white_best_statue(self):
        # Potions always drop after combat.
        relic = WhiteBestStatue(self.player)
        self.player.add_relic(relic)

    @unittest.skip("TODO: Implement shops")
    def test_the_courier(self):
        # The merchant no longer runs out of cards, relics, or potions and his prices are reduced by 20%.
        relic = TheCourier(self.player)
        self.player.add_relic(relic)


