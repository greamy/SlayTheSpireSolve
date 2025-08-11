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
from GameSim.Map.MonsterRoom import MonsterRoom
from GameSim.Render.Renderer import Renderer


class GameTest(unittest.TestCase):

    def setUp(self):
        # self.renderer = Renderer()
        self.renderer = Renderer(render_type=Renderer.RenderType.PYGAME)
        random.seed(42)

    def test_render_playable_game(self):
        controller = RenderInputPlayerController(self.renderer.screen)
        self.game = Game(controller, self.renderer)
        self.game.run()

    def test_render_viewable_game(self):
        controller = RandomPlayerController(delay=1)
        self.game = Game(controller, self.renderer)
        self.game.run()

    def test_simple_bot_game(self):
        controller = SimpleBotPlayerController(delay=1)
        self.game = Game(controller, self.renderer)
        self.game.run()

    def test_simple_bot_many_games(self):
        controller = SimpleBotPlayerController(delay=0)
        self.run_many_games(controller)

    def test_random_bot_many_games(self):
        controller = RandomPlayerController(delay=0)

        self.run_many_games(controller)

    def test_simple_vs_random(self):
        simple_controller = SimpleBotPlayerController(delay=0)
        random_controller = RandomPlayerController(delay=0)
        combat_type = "monster"
        number_of_combats = 1000
        history = self.run_many_games(simple_controller, combat_type, number_of_combats)
        random_hist = self.run_many_games(random_controller, combat_type, number_of_combats)
        visualize_bot_comparison(history, random_hist)

    def test_PPO_bot(self):
        rl_controller = RLPlayerController(delay=1, train=True)
        self.game = Game(rl_controller, self.renderer)
        self.game.run()

    def test_train_PPO_bot(self):
        rl_controller = RLPlayerController(delay=0, train=True)
        self.run_many_games(rl_controller, "monster", 1000)
        plt.plot(rl_controller.final_healths, color='tab:blue', marker='x', linestyle='-', label='Average Reward')
        plt.xlabel('Learning Period', fontsize=12)
        plt.ylabel('Average Reward', fontsize=12)
        plt.title('Training Rewards Over Time', fontsize=14)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()

        plt.savefig("../images/model_results/first_fight/final_healths.png")