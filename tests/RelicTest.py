import unittest

from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.Akabeko import Akabeko
from CombatSim.Items.Relics.DisplayCase.Anchor import Anchor
from CombatSim.Items.Relics.DisplayCase.HolyWater import HolyWater
from CombatSim.Items.Relics.DisplayCase.Orichalcum import Orichalcum


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
        relic = Akabeko(self.player)
        card = Strike(self.player)
        self.player.add_relic(relic)
        self.player.start_turn(self.enemies, self.debug)
        self.player.deck.hand.append(card)
        self.player.play_card(card,self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health, self.enemy_start_health-(card.damage+8))
        self.player.deck.hand.append(card)
        self.player.play_card(card, self.enemy, self.enemies, self.debug)
        self.assertEqual(self.enemy.health,self.enemy_start_health-(card.damage+8)-card.damage )






