import os
import random
import unittest
import copy

from numpy.ma.testutils import assert_not_equal

from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Entities.Dungeon.GremlinNob import GremlinNob
from CombatSim.Entities.Dungeon.Sentry import Sentry
from CombatSim.Entities.Dungeon.Taskmaster import Taskmaster
from CombatSim.Entities.Player import Player
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
        self.player = createPlayer(lib_path='CombatSim/Actions/Library')
        self.player_start_health = self.player.health
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
            self.enemy.do_turn(self.player, self.debug) # chooses new intent
            self.assertEqual(self.enemy.block, self.last_intent.block)
            self.enemy.start_turn([self.player], self.debug)
            self.assertEqual(self.player.health, current_health - self.last_intent.damage)

            if self.last_intent.name == "Bellow":
                self.enemy.damage_dealt_modifier = 5


    def test_Taskmaster(self):
        self.enemy = Taskmaster(self.ascension, self.act)
        intents_played = []
        for intent in self.enemy.intent_set:
            self.enemy.intent = intent
            current_health = self.player.health
            self.last_intent = self.enemy.intent
            self.enemy.do_turn(self.player, self.debug) # chooses new intent
            self.assertEqual(self.enemy.block, self.last_intent.block)
            self.enemy.start_turn([self.player], self.debug)
            self.assertEqual(self.player.health, current_health - self.last_intent.damage)


    def test_gremlin_nob(self):
        self.enemy = GremlinNob(self.ascension, self.act)
        # addCards(self.player, get_default_deck())

        for intent in self.enemy.intent_set:
            self.enemy.intent = intent
            current_health = self.player.health
            self.last_intent = self.enemy.intent
            self.enemy.do_turn(self.player, self.debug)  # chooses new intent
            if self.last_intent == 'Bellow':
                card = Defend(self.player)
                self.player.deck.hand.append(card)
                self.player.play_card(card)
                self.assertEqual(self.enemy.damage_dealt_modifier, self.enemy.enrage)
                self.enemy.damage_dealt_modifier -= self.enemy.enrage
            elif self.last_intent.name == 'SkullBash':
                self.assertEqual(self.player.damage_taken_multiplier, Vulnerable.MULT)
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
            self.enemy.do_turn(self.player, self.debug)  # chooses new intent
            if self.last_intent.name == 'Bolt':
                self.assertIn('Dazed', [card.name for card in self.player.deck.discard_pile])
            else:
                self.assertEqual(self.player.health, current_health - self.last_intent.damage)

