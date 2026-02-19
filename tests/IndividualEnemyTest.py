import math
import os
import random
import unittest
import copy

from numpy.ma.testutils import assert_not_equal

from CombatSim.Actions.Library.Brilliance import Brilliance
from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Actions.Library.Wound import Wound
from CombatSim.Entities.Dungeon.Cultist import Cultist
from CombatSim.Entities.Dungeon.FatGremlin import FatGremlin
from CombatSim.Entities.Dungeon.FungiBeast import FungiBeast
from CombatSim.Entities.Dungeon.GreenLouse import GreenLouse
from CombatSim.Entities.Dungeon.GremlinNob import GremlinNob
from CombatSim.Entities.Dungeon.Lagavulin import Lagavulin
from CombatSim.Entities.Dungeon.Looter import Looter
from CombatSim.Entities.Dungeon.RedLouse import RedLouse
from CombatSim.Entities.Dungeon.Sentry import Sentry
from CombatSim.Entities.Dungeon.ShieldGremlin import ShieldGremlin
from CombatSim.Entities.Dungeon.SneakyGremlin import SneakyGremlin
from CombatSim.Entities.Dungeon.Taskmaster import Taskmaster
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Status.Frail import Frail
from CombatSim.Entities.Status.Weak import Weak
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.util import createPlayer, addCards, get_default_deck
from GameSim.Input.RandomPlayerController import RandomPlayerController

from CombatSim.Entities.Dungeon.JawWorm import JawWorm


class IndividualEnemyTest(unittest.TestCase):

    def setUp(self):
        self.health = 72
        self.energy = 3
        self.gold = 100
        # self.player = Player(self.health, self.energy, self.gold, [], [], [],
        #                      RandomPlayerController(), library_path="/home/grant/PycharmProjects/SlayTheSpireSolve/CombatSim/Actions/Library")
        # test Lucas Library path -> 'C:/Users/Owner/PycharmProjects/SlayTheSpireSolve/CombatSim/Actions/Library'
        self.lib_path = 'CombatSim/Actions/Library'
        self.player = createPlayer(lib_path=self.lib_path, max_health=self.health, health=self.health)
        self.ascension = 20
        self.act = 1
        # self.enemy = JawWorm(self.ascension, self.act)
        # self.enemy_start_health = self.enemy.health
        #
        # self.enemies = [self.enemy]
        self.debug = False

    def test_JawWorm(self):
        self.enemy = JawWorm(self.ascension, self.act)
        for intent in self.enemy.intent_set:
            self.enemy.intent = intent
            current_health = self.player.health
            self.last_intent = self.enemy.intent
            self.enemy.do_turn([self.enemy], [self.player], self.debug) # chooses new intent
            self.assertEqual(self.enemy.block, self.last_intent.block)
            self.enemy.start_turn([self.player], self.debug)
            self.assertEqual(self.player.health, current_health - self.last_intent.damage)

            if self.last_intent.name == "Bellow":
                self.enemy.damage_dealt_modifier = 5


    def test_Taskmaster(self):
        self.enemy = Taskmaster(self.ascension, self.act)
        self.assertTrue(self.enemy.intent, self.enemy.intent_set[self.enemy.SCOURINGWHIP])
        self.enemy.do_turn([self.enemy], [self.player],self.debug)
        self.assertTrue(self.player.health, self.player.start_health - self.enemy.intent_set[self.enemy.SCOURINGWHIP].damage)
        self.assertEqual(len(self.player.deck.discard_pile), self.enemy.intent_set[self.enemy.SCOURINGWHIP].wounds_added)
        self.assertIn('Wound', [card.name for card in self.player.deck.discard_pile])
        self.assertTrue(self.enemy.damage_dealt_modifier, self.enemy.intent_set[self.enemy.SCOURINGWHIP].strength)


    def test_gremlin_nob(self):
        self.enemy = GremlinNob(self.ascension, self.act)
        # addCards(self.player, get_default_deck())

        for intent in self.enemy.intent_set:
            self.enemy.intent = intent
            current_health = self.player.health
            self.last_intent = self.enemy.intent
            self.enemy.do_turn([self.enemy], [self.player], self.debug)  # chooses new intent
            if self.last_intent.name == 'Bellow':
                card = Defend(self.player)
                self.player.deck.hand.append(card)
                self.player.play_card(card, self.enemy, [self.enemy], self.debug)
                self.player.block = 0
                self.assertEqual(self.enemy.damage_dealt_modifier, self.enemy.enrage)
                self.enemy.damage_dealt_modifier -= self.enemy.enrage
            elif self.last_intent.name == 'SkullBash':
                self.assertEqual(self.player.damage_taken_multiplier, Vulnerable.DAMAGE_TAKEN_MULTIPLIER)
                self.assertEqual(self.player.health,
                                 current_health - (self.last_intent.damage))
            else:
                self.assertEqual(self.player.health,
                                 current_health - (self.last_intent.damage * self.player.damage_taken_multiplier))


    def test_Sentry(self):
        self.enemy = Sentry(self.ascension, self.act)
        # addCards(self.player, get_default_deck())

        for intent in self.enemy.intent_set:
            self.enemy.intent = intent
            current_health = self.player.health
            self.last_intent = self.enemy.intent
            self.enemy.do_turn([self.enemy], [self.player], self.debug)  # chooses new intent
            if self.last_intent.name == 'Bolt':
                self.assertIn('Dazed', [card.name for card in self.player.deck.discard_pile])
            else:
                self.assertEqual(self.player.health, current_health - self.last_intent.damage)


    def test_lagavulin(self):
        self.enemy = Lagavulin(self.ascension, self.act)
        self.assertEqual(self.enemy.block, 8)
        self.last_intent = self.enemy.intent
        self.enemy.start_turn([self.player], self.debug)
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.enemy.block, self.enemy.metallicize_amount)

        # Turn 2 and Turn 3 - Asleep
        self.enemy.start_turn([self.player], self.debug)
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.enemy.start_turn([self.player], self.debug)
        self.enemy.do_turn([self.enemy], [self.player], self.debug)

        # Turn 4 - Should wake up and attack
        self.enemy.start_turn([self.player], self.debug)
        self.assertTrue(self.enemy.intent == self.enemy.intent_set[Lagavulin.ATTACK])
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.health, self.player.start_health - self.enemy.intent_set[Lagavulin.ATTACK].damage)

        # Turn 5 - Should wake up and attack
        current_health = self.player.health
        self.enemy.start_turn([self.player], self.debug)
        self.assertTrue(self.enemy.intent == self.enemy.intent_set[Lagavulin.ATTACK])
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.health, current_health - self.enemy.intent_set[Lagavulin.ATTACK].damage)

        # Turn 6 - DEBUFF
        self.enemy.start_turn([self.player], self.debug)
        self.assertTrue(self.enemy.intent == self.enemy.intent_set[Lagavulin.SIPHONSOUL])
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.damage_dealt_modifier, -self.enemy.intent_set[Lagavulin.SIPHONSOUL].debuff)
        card = Defend(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card,self.enemy, self.enemy, self.debug )
        self.assertEqual(self.player.block, card.block - self.enemy.intent_set[Lagavulin.SIPHONSOUL].debuff)
        self.player.damage_dealt_modifier += self.enemy.intent_set[Lagavulin.SIPHONSOUL].debuff # resetting for next combat

        # new combat
        self.enemy2 = Lagavulin(self.ascension, self.act)
        # print([self.enemy2.start_health, self.enemy2.health])
        self.player.health = self.player.start_health
        self.player.deck.discard_pile.remove(card)
        self.assertEqual(self.enemy2.intent, self.enemy2.intent_set[Lagavulin.SLEEP])

        card = Brilliance(self.player)
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy2, self.enemy2, self.debug)
        # print([self.enemy2.health, self.enemy2.start_health])
        self.assertEqual(self.enemy2.health, self.enemy2.start_health + self.enemy2.metallicize_amount - card.damage)
        self.enemy2.do_turn([self.enemy2], [self.player], self.debug)
        self.assertFalse(self.enemy2.sleeping)
        self.assertTrue(self.enemy2.intent == self.enemy2.intent_set[Lagavulin.ATTACK])

    def test_cultist(self):
        self.enemy = Cultist(self.ascension, self.act)

        self.assertEqual(self.enemy.intent, self.enemy.intent_set[self.enemy.INCANTATION])
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.enemy.damage_dealt_modifier, 0)
        self.assertEqual(self.enemy.intent, self.enemy.intent_set[self.enemy.DARKSTRIKE])
        self.assertEqual(self.enemy.intent_set[self.enemy.INCANTATION].ritual, 5) # 5 is A20 number
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.health,
                         self.player.start_health - self.enemy.intent_set[self.enemy.DARKSTRIKE].damage)
        self.assertEqual(self.enemy.damage_dealt_modifier, self.enemy.intent_set[self.enemy.INCANTATION].ritual)


    def test_greenlouse(self):
        for _ in range(100):
            self.enemy = GreenLouse(self.ascension, self.act)
            self.player = createPlayer(lib_path=self.lib_path, max_health=self.health)
            for intent in self.enemy.intent_set:
                if intent.name == "Bite":
                    start_health = self.player.health
                    self.enemy.intent = intent
                    self.enemy.do_turn([self.enemy], [self.player], self.debug)
                    self.assertEqual(start_health - self.player.health, self.enemy.D)
                    self.player.health = self.player.start_health
                if intent.name == "SpitWeb":
                    self.enemy.intent = intent
                    start_health = self.enemy.health
                    self.enemy.do_turn([self.enemy], [self.player], self.debug)
                    card = Strike(self.player)
                    strike1 = self.player.add_card("Strike")
                    strike2 = self.player.add_card("Strike")
                    self.player.begin_combat([self.enemy], self.debug)
                    self.player.start_turn([self.enemy], self.debug)
                    self.player.play_card(strike1, self.enemy,[self.enemy], self.debug)
                    # test curl up mechanic
                    self.assertTrue(self.enemy.block == self.enemy.curl_up)
                    self.assertTrue(self.enemy.curl_up_used)

                    block = self.enemy.block
                    self.assertTrue(self.player.damage_dealt_multiplier, Weak.DAMAGE_DEALT_MULTIPLIER)
                    self.assertEqual(self.enemy.health, start_health - math.floor(card.damage * self.player.damage_dealt_multiplier))

                    self.player.play_card(strike2, self.enemy, [self.enemy], self.debug)

                    self.assertEqual(self.enemy.block, block - math.floor(strike2.damage * self.player.damage_dealt_multiplier))

    def test_redlouse(self):
        for _ in range(100):
            self.enemy = RedLouse(self.ascension, self.act)
            self.player = createPlayer(lib_path=self.lib_path, max_health=self.health)
            for intent in self.enemy.intent_set:
                if intent.name == "Bite":
                    start_health = self.player.health
                    self.enemy.intent = intent
                    self.enemy.do_turn([self.enemy], [self.player], self.debug)
                    self.assertEqual(start_health - self.player.health, self.enemy.D)
                    self.player.health = self.player.start_health
                    
                    # test curl up
                    strike1 = self.player.add_card("Strike")
                    strike2 = self.player.add_card("Strike")
                    
                    self.player.begin_combat([self.enemy], self.debug)
                    self.player.start_turn([self.enemy], self.debug)
                    self.player.play_card(strike1, self.enemy, [self.enemy], self.debug)
                    self.assertEqual(self.enemy.block, self.enemy.curl_up)
                    self.assertTrue(self.enemy.curl_up_used)
                    block = self.enemy.block
                    self.player.play_card(strike2, self.enemy, [self.enemy], self.debug)
                    self.assertEqual(self.enemy.block, block - math.floor(strike2.damage * self.player.damage_dealt_multiplier))
                if intent.name == "Grow":
                    self.enemy.intent = intent
                    self.enemy.do_turn([self.enemy], [self.player], self.debug)
                    self.assertEqual(self.enemy.damage_dealt_modifier, self.enemy.intent_set[self.enemy.GROW].strength_gain)
                    self.enemy.damage_dealt_modifier -= self.enemy.intent_set[self.enemy.GROW].strength_gain

    def test_FatGremlin(self):
        self.enemy = FatGremlin(self.ascension, self.act)
        self.enemy.choose_intent()

        self.enemy.do_turn([self.enemy], [self.player], self.debug)

        self.assertTrue(self.player.health == self.player.start_health - self.enemy.intent_set[self.enemy.SMASH].damage)

        self.assertEqual(len(self.player.status_list), 2) # in A20 Fat gremlin applies weak and frail
        status_ids = [status.ID for status in self.player.status_list]
        self.assertIn(Frail.ID, status_ids)
        self.assertIn(Weak.ID, status_ids)


    def test_looter(self):
        self.enemy = Looter(self.ascension, self.act)
        enemies = [self.enemy]
        for intent in self.enemy.intent_set:
            if intent.name == "Mug":
                self.enemy.intent = intent
                self.player.health = self.player.start_health
                self.player.gold = 25
                gold_start = 25
                start_health = self.player.health
                self.enemy.do_turn(enemies, [self.player], self.debug)
                self.assertEqual(self.player.health, start_health - self.enemy.intent_set[self.enemy.MUG].damage)
                self.assertEqual(self.player.gold, gold_start - self.enemy.thievery)
            if intent.name == "Lunge":
                self.enemy.intent = intent
                self.player.health = self.player.start_health
                self.player.gold = 25
                gold_start = 25
                start_health = self.player.health
                self.enemy.do_turn(enemies, [self.player], self.debug)
                self.assertEqual(self.player.health, start_health - self.enemy.intent_set[self.enemy.LUNGE].damage)
                self.assertEqual(self.player.gold, gold_start - self.enemy.thievery)
            if intent.name == "SmokeBomb":
                self.enemy.intent = intent
                self.enemy.do_turn(enemies, [self.player], self.debug)
                self.assertEqual(self.enemy.block, self.enemy.intent_set[self.enemy.SMOKEBOMB].block)
            if intent.name == "Escape":
                self.enemy.intent = intent
                self.enemy.do_turn(enemies, [self.player], self.debug)
                self.assertNotIn(self.enemy, enemies)



        # new combat
        self.player = createPlayer(lib_path=self.lib_path, max_health=self.health)
        self.player.gold = 25
        self.enemy = Looter(self.ascension, self.act)
        self.enemy.intent = self.enemy.intent_set[self.enemy.MUG]
        self.enemy.do_turn([self.enemy], [self.player], self.debug)
        self.assertEqual(self.player.gold, 25 - self.enemy.thievery)
        self.player.damage_dealt_multiplier += 50
        strike = Strike(self.player)
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, [self.enemy], self.debug)
        print(strike.damage * self.player.damage_dealt_multiplier)
        print(self.enemy.health)
        self.assertEqual(self.player.gold, 25)


    def test_fungibeast(self):
        self.enemy = FungiBeast(self.ascension, self.act)
        for intent in self.enemy.intent_set:
            if intent.name == "Bite":
                self.enemy.intent = intent
                self.enemy.do_turn([self.enemy], [self.player], self.debug)
                self.assertEqual(self.player.health, self.player.start_health - self.enemy.intent_set[self.enemy.BITE].damage)
            if intent.name =="Grow":
                self.enemy.intent = intent
                self.enemy.do_turn([self.enemy], [self.player], self.debug)
                self.assertEqual(self.enemy.damage_dealt_modifier, self.enemy.intent_set[self.enemy.GROW].strength)
                self.enemy.damage_dealt_modifier = 0

        strike = Strike(self.player)
        self.player.damage_dealt_multiplier += 50
        self.player.deck.hand.append(strike)
        self.player.play_card(strike, self.enemy, [self.enemy], self.debug)
        status_ids = [status.ID for status in self.player.status_list]
        self.assertIn(Vulnerable.ID, status_ids)

    def test_sneaky_gremlin(self):
        self.enemy = SneakyGremlin(self.ascension, self.act)
        for intent in self.enemy.intent_set:
            if intent.name == "Puncture":
                self.enemy.intent = intent
                self.enemy.do_turn([self.enemy], [self.player], self.debug)
                self.assertEqual(self.player.health, self.player.start_health - self.enemy.intent_set[self.enemy.PUNCTURE].damage)

    def test_shield_gremlin(self):
        self.enemy = ShieldGremlin(self.ascension, self.act)
        other_enemy = SneakyGremlin(self.ascension, self.act)
        enemies = [self.enemy, other_enemy]
        self.enemy._set_intent(self.enemy.PROTECT)
        for i in range(10):
            self.enemy.do_turn(enemies, [self.player], self.debug) # guaranteed to choose protect every time while other enemy in combat
            self.assertTrue(self.enemy.block == 0)
            self.assertTrue(other_enemy.block == self.enemy._get_intent(self.enemy.PROTECT).block)
            for e in enemies:
                e.block = 0
        enemies = [self.enemy]
        self.enemy.do_turn(enemies, [self.player], self.debug)
        self.assertTrue(self.enemy.block == self.enemy._get_intent(self.enemy.PROTECT).block)
        self.assertTrue(self.enemy.intent == self.enemy._get_intent(self.enemy.SHIELDBASH))
        self.enemy.do_turn(enemies, [self.player], self.debug)
        self.assertTrue(self.player.health == self.player.start_health - self.enemy._get_intent(self.enemy.SHIELDBASH).damage)











