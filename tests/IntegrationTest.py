import random
import unittest
import matplotlib.pyplot as plt
import numpy as np

from CombatSim.Actions.Library.Devotion import Devotion
from CombatSim.Actions.Library.EmptyBody import EmptyBody
from CombatSim.Actions.Library.Prostrate import Prostrate
from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.PureWater import PureWater
from CombatSim.util import createPlayer, addCards, get_default_deck, visualize_bot_comparison
from GameSim.Game import Game
from GameSim.Input.RLPlayerController import RLPlayerController
from GameSim.Input.RandomPlayerController import RandomPlayerController
from GameSim.Input.RenderInputController import RenderInputPlayerController
from GameSim.Input.SimpleBotPlayerController import SimpleBotPlayerController
from GameSim.Map.CombatRoom import CombatRoom
from GameSim.Map.EliteRoom import EliteRoom
from GameSim.Map.Map import Map
from GameSim.Map.MapGenerator import MapGenerator
from GameSim.Map.MonsterRoom import MonsterRoom
from GameSim.Render.Renderer import Renderer


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        # self.renderer = Renderer()
        self.renderer = Renderer(render_type=Renderer.RenderType.NONE)

        self.health = 100
        self.energy = 3
        self.gold = 100
        self.controller = RandomPlayerController(delay=0)
        self.lib_path = "CombatSim/Actions/Library"
        self.relic_path = "CombatSim/Items/Relics/DisplayCase"
        self.player = Player(self.health, self.energy, self.gold, [], [], [], self.controller,
                             library_path=self.lib_path, relic_path=self.relic_path)

        random.seed(42)

    def test_map_choices(self):
        self.controller = RLPlayerController("artifacts/images/model_results/tests/", delay=0)
        map_gen = MapGenerator(self.player, 1, 20, 42)
        map = map_gen.generate_map()
        # controller = RenderInputPlayerController(self.renderer.screen)
        self.controller.get_map_choice(self.player, map, 0, None)
