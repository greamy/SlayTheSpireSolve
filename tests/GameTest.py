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
from CombatSim.util import createPlayer, addCards, get_default_deck
from GameSim.Game import Game
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
                enemy_choice = enemies[i]
            else:
                room.start()
                enemy_choice = room.player.last_elite

            print(f"*********************** Fighting {enemy_choice}! {i}/{num_combats} ************************")
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
        self.visualize_bot_comparison(history, random_hist)


    def visualize_bot_comparison(self, simple_history, random_history):
        """
        Visualize the win rate comparison between simple bot and random bot

        Args:
            simple_history: Dict with enemy names as keys, [wins, total_combats] as values
            random_history: Dict with enemy names as keys, [wins, total_combats] as values
        """

        # Get all unique enemies from both histories
        all_enemies = set(simple_history.keys()) | set(random_history.keys())
        all_enemies = sorted(list(all_enemies))

        # Calculate win percentages for each bot
        simple_win_rates = []
        random_win_rates = []

        for enemy in all_enemies:
            # Simple bot win rate
            if enemy in simple_history:
                wins, total = simple_history[enemy]
                simple_rate = (wins / total) * 100 if total > 0 else 0
            else:
                simple_rate = 0
            simple_win_rates.append(simple_rate)

            # Random bot win rate
            if enemy in random_history:
                wins, total = random_history[enemy]
                random_rate = (wins / total) * 100 if total > 0 else 0
            else:
                random_rate = 0
            random_win_rates.append(random_rate)

        # Set up the bar chart
        x = np.arange(len(all_enemies))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 8))

        # Create bars
        bars1 = ax.bar(x - width / 2, simple_win_rates, width, label='Simple Bot',
                       color='skyblue', alpha=0.8)
        bars2 = ax.bar(x + width / 2, random_win_rates, width, label='Random Bot',
                       color='lightcoral', alpha=0.8)

        # Add value labels on bars
        def add_value_labels(bars, values):
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                        f'{value:.1f}%', ha='center', va='bottom', fontsize=8)

        add_value_labels(bars1, simple_win_rates)
        add_value_labels(bars2, random_win_rates)

        # Customize the chart
        ax.set_xlabel('Enemy Types', fontsize=12, fontweight='bold')
        ax.set_ylabel('Win Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Bot Performance Comparison: Win Rates Against Different Enemies',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(all_enemies, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 105)  # Set y-axis limit to show percentages clearly

        # Add overall statistics
        simple_overall = np.mean(simple_win_rates)
        random_overall = np.mean(random_win_rates)

        ax.text(0.02, 0.98, f'Simple Bot Average: {simple_overall:.1f}%\nRandom Bot Average: {random_overall:.1f}%',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.tight_layout()
        plt.show()
