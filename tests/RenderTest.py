import unittest
import pygame

from Combat import Combat
from CombatSim.Renderer import Renderer
from CombatSim.util import addCards, createPlayer, createEnemy


class RenderTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

        self.debug = False

        cards = ["Strike" for _ in range(4)]
        cards.extend(["Defend" for _ in range(4)])
        cards.extend(["Vigilance", "Eruption"])
        cards.extend(["Devotion" for _ in range(5)])
        cards.extend(["SandsofTime" for _ in range(2)])
        self.player = createPlayer()
        addCards(self.player, cards)

        self.enemy = createEnemy("SlimeBoss", 20, 1)

    def test_render(self):
        testing_enemy = createEnemy("Hexaghost", 20, 1)
        testing_player = self.player
        combat = Combat(testing_player, [testing_enemy], True)
        combat.start()
        renderer = Renderer(self.screen, combat)
        renderer.render_combat()

    def test_playable_render(self):
        enemy = createEnemy("AcidSlimeSmall", 20, 1)
        player = self.player
        combat = Combat(player, [enemy], True)
        combat.start()

        renderer = Renderer(self.screen, combat)
        renderer.render_playable_combat()
