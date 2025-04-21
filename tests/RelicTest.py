import unittest

from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.Anchor import Anchor
from CombatSim.Items.Relics.DisplayCase.HolyWater import HolyWater


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
        self.assertEqual(self.player.block, 10)


