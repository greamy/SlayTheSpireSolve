import unittest
import pygame

from Combat import Combat
from CombatSim.Map.MapGenerator import MapGenerator
from CombatSim.Renderer import Renderer
from CombatSim.util import addCards, createPlayer, createEnemy


class RenderTest(unittest.TestCase):

    def setUp(self):

        self.debug = False

        cards = ["Strike" for _ in range(4)]
        cards.extend(["Defend" for _ in range(4)])
        cards.extend(["Vigilance", "Eruption"])
        cards.extend(["Devotion" for _ in range(5)])
        cards.extend(["SandsofTime" for _ in range(2)])
        self.player = createPlayer()
        addCards(self.player, cards)

        self.enemy = createEnemy("SlimeBoss", 20, 1)
        self.combat = Combat(self.player, [self.enemy], True)
        self.renderer = Renderer(self.combat)

    def test_render(self):
        self.combat.start()
        renderer = Renderer(self.combat)
        renderer.render_combat()

    def test_playable_render(self):
        self.combat.start()

        renderer = Renderer(self.screen, self.combat)
        renderer.render_playable_combat()

    def test_render_map(self):
        map_gen = MapGenerator()
        map_gen.generate_map()

        renderer = Renderer(self.combat)
        renderer.render_map(map_gen)

