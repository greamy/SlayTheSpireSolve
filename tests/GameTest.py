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

    def run_many_games(self, controller, combat_type="monster", num_combats=5000):
        renderer = Renderer(render_type=Renderer.RenderType.NONE)

        possible_enemies = Enemy.get_implemented_enemies("../CombatSim/Entities/Dungeon/")
        # print(possible_enemies)

        random.seed(42)
        enemies = []
        if combat_type == "monster":
            rooms = [MonsterRoom(createPlayer(controller=controller, cards=[]), 1, 0, [], [], random.randint(1, 2), 20) for i in range(num_combats)]
        elif combat_type == "elite":
            rooms = [EliteRoom(createPlayer(controller=controller, cards=[]), 1, 0, [], [], random.randint(1, 2), 20) for i in range(num_combats)]
        else:
            rooms = []
        for room in rooms:
            cards = get_default_deck()
            cards.remove("Defend")
            cards.remove("Defend")
            cards.extend(["Prostrate", "Worship", "EmptyBody", "CutThroughFate", "FollowUp", "JustLucky", "MentalFortress", "Wallop", "Tranquility", "Crescendo"])
            addCards(room.player, cards)

            room.player.add_relic(PureWater(room.player))

            if combat_type == "monster":
                enemy_choice = random.choice(list(possible_enemies.keys()))
                try:
                    enemy_ = getattr(possible_enemies[enemy_choice], enemy_choice)
                    room.enemies = [enemy_(ascension=20, act=1)]
                    enemies.append(enemy_choice)
                except AttributeError:
                    room.enemies = [AcidSlimeSmall(20, 1)]
                    enemies.append("AcidSlimeSmall")
        num_wins = 0
        enemy_combats = {}

        for i, room in enumerate(rooms):
            if combat_type == "monster":
                room.player.begin_combat(room.enemies, False)
                room.player.start_turn(room.enemies, False)
                room.player.controller.begin_combat(room.player, room.enemies, False)
                enemy_choice = enemies[i]
            else:
                room.start()
                enemy_choice = room.player.last_elite

            # print(f"*********************** Fighting {enemy_choice}! {i}/{num_combats} ************************")
            renderer.render_room(room)

            if room.player.is_alive():
                num_wins += 1
                if enemy_choice in enemy_combats.keys():
                    enemy_combats[enemy_choice][0] += 1
                    enemy_combats[enemy_choice][1] += 1
                else:
                    enemy_combats[enemy_choice] = [1, 1]
            else:
                if enemy_choice in enemy_combats.keys():
                    enemy_combats[enemy_choice][1] += 1
                else:
                    enemy_combats[enemy_choice] = [0, 1]
        print(f"Win rate: {num_wins / 1000}")
        for key in sorted(enemy_combats.keys()):
            print(f"{key}: {enemy_combats[key]}")
        return enemy_combats

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
