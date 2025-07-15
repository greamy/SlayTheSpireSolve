import unittest

from GameSim.Game import Game
from GameSim.Input.RenderInputController import RenderInputPlayerController
from GameSim.Render.Renderer import Renderer


class GameTest(unittest.TestCase):

    def setUp(self):
        self.renderer = Renderer()

    def test_render_playable_game(self):
        controller = RenderInputPlayerController(self.renderer.screen)
        self.game = Game(controller, self.renderer)
        self.game.run()
