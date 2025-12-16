import os
import random
import unittest
import copy
from CombatSim.Entities.Player import Player
from CombatSim.util import createPlayer
from GameSim.Input.RandomPlayerController import RandomPlayerController

from CombatSim.Entities.Dungeon.JawWorm import JawWorm





class IndividualEnemyTest(unittest.TestCase):

    def setUp(self):
        self.health = 100
        self.energy = 3
        self.gold = 100
        # TODO: Define a player controller for tests - always chooses first enemy, always discards scry, etc.
        # TODO: Use this to get consistent test results for scrying and testing against multiple enemies.
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
        intents_played = []
        # while len(intents_played) < len(self.enemy.intent_set):
        a = 0
        while a == 0:
            if self.enemy.intent not in intents_played:
                intents_played.append(self.enemy.intent)
                self.last_intent = self.enemy.intent
                self.enemy.do_turn(self.player, self.debug)

                self.assertEqual(self.player.health, self.player_start_health - self.last_intent.damage)
                a += 1
            else:
                self.enemy.choose_intent()






