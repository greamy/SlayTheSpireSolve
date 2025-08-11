import importlib
import random

import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

from CombatSim.Actions.Library.Defend import Defend
from CombatSim.Actions.Library.Strike import Strike
from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.DisplayCase.PureWater import PureWater
from GameSim.Input.RandomPlayerController import RandomPlayerController
from GameSim.Map.EliteRoom import EliteRoom
from GameSim.Map.MonsterRoom import MonsterRoom
from GameSim.Render.Renderer import Renderer


def addCards(player, name_list: list[str]):
    cards = []
    for name in name_list:
        module = importlib.import_module("CombatSim.Actions.Library." + name)
        class_ = getattr(module, name)
        card = class_(player)
        cards.append(card)
    player.deck = Player.Deck(cards)


def createPlayer(lib_path='../CombatSim/Actions/Library', controller=RandomPlayerController(),
                 health=70, energy=3, gold=50, potions=None, relics=None, cards=None):
    if relics is None:
        relics = []
    if potions is None:
        potions = []
    if cards is None:
        cards = []
    return Player(health, energy, gold, potions, relics, cards, controller, lib_path)


def createEnemy(name: str, ascension: int, act: int):
    module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
    class_ = getattr(module, name)
    return class_(ascension, act)

def get_default_deck():
    cards = ["Strike" for _ in range(4)]
    cards.extend(["Defend" for _ in range(4)])
    cards.extend(["Vigilance", "Eruption"])
    # cards.extend(["Devotion" for _ in range(5)])
    # cards.extend(["SandsofTime" for _ in range(2)])
    return cards

def visualize_bot_comparison(simple_history, random_history):
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

def visualize_bot_history(loss_hist, reward_hist, filepath):
    """
    Visualize the win rate comparison between simple bot and random bot

    Args:
        loss_hist: List of avg loss each learning period of PPO
        reward_hist: List of avg rewards from each learning period of PPO
    """

    # --- Input Validation ---
    if not loss_hist or not reward_hist:
        print("Error: loss_hist and reward_hist cannot be empty.")
        return
    if len(loss_hist) != len(reward_hist):
        print("Error: loss_hist and reward_hist must have the same length.")
        return

    # --- Plotting ---
    try:
        # Create a figure and a set of subplots.
        # `fig` is the entire figure, and `ax1`, `ax2` are the individual plots.
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        fig.suptitle('Bot Training History', fontsize=16, fontweight='bold')

        # --- Plot 1: Average Loss History ---
        ax1.plot(loss_hist, color='tab:red', marker='o', linestyle='-', label='Average Loss')
        ax1.set_ylabel('Average Loss', fontsize=12)
        ax1.set_title('Training Loss Over Time', fontsize=14)
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax1.legend()

        # --- Plot 2: Average Reward History ---
        ax2.plot(reward_hist, color='tab:blue', marker='x', linestyle='-', label='Average Reward')
        ax2.set_xlabel('Learning Period', fontsize=12)
        ax2.set_ylabel('Average Reward', fontsize=12)
        ax2.set_title('Training Rewards Over Time', fontsize=14)
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax2.legend()

        # --- Final Touches ---
        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the suptitle

        # Save the figure to the specified file path
        plt.savefig(filepath)
        print(f"Plot successfully saved to {filepath}")

        # Close the plot to free up memory
        plt.close(fig)

    except Exception as e:
        print(f"An error occurred during plotting: {e}")

def visualize_embeddings(card_names, embeddings, perplexity=5, random_state=42):
    """
    Visualize a numpy array of embeddings with a dimension-reduction technique
    to graph each card in two dimensions.

    :param card_names: A list of strings, where each string is the name of a card.
    :param embeddings: A numpy array of shape (n_cards, n_dimensions) containing the embeddings.
    :param perplexity: The perplexity value for the t-SNE algorithm. It is related to the
                       number of nearest neighbors that is taken into account for each point.
    :param random_state: The seed for the random number generator to ensure reproducibility.
    """
    if len(card_names) != embeddings.shape[0]:
        raise ValueError("The number of card names must match the number of embeddings.")

    # --- 1. Dimensionality Reduction with t-SNE ---
    # t-SNE is a great technique for visualizing high-dimensional data in 2D or 3D.
    # It tries to preserve the local structure of the data, so points that are close
    # in the high-dimensional space will be close in the low-dimensional space.
    print("Performing t-SNE dimensionality reduction...")
    tsne = TSNE( # ai wrote this whole function ...
        n_components=2,
        perplexity=perplexity,
        random_state=random_state,
        init='pca',
        learning_rate='auto',
        max_iter=1000
    )
    embeddings_2d = tsne.fit_transform(embeddings)
    print("Reduction complete.")

    # --- 2. Create the Scatter Plot ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 10))

    # Scatter plot of the 2D embeddings
    ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.7, edgecolors='w', s=100)

    # --- 3. Add Annotations (Card Names) ---
    # Annotate each point with its corresponding card name for clarity.
    for i, name in enumerate(card_names):
        ax.annotate(name, (embeddings_2d[i, 0], embeddings_2d[i, 1]), fontsize=9, alpha=0.85)

    # --- 4. Final Touches ---
    ax.set_title('2D Visualization of Card Embeddings using t-SNE', fontsize=16)
    ax.set_xlabel('t-SNE Dimension 1', fontsize=12)
    ax.set_ylabel('t-SNE Dimension 2', fontsize=12)
    plt.grid(True)
    plt.savefig("artifacts/images/model_results/first_fight/embed_vis.png")
    plt.clf()


def run_many_games(controller, dungeon_path, library_path, render_type=Renderer.RenderType.NONE, combat_type="monster", num_combats=5000):
    renderer = Renderer(render_type=render_type)

    possible_enemies = Enemy.get_implemented_enemies(dungeon_path)
    # print(possible_enemies)

    random.seed(42)
    enemies = []
    if combat_type == "monster":
        rooms = [MonsterRoom(createPlayer(controller=controller, cards=[], lib_path=library_path), 1, 0, [], [], random.randint(1, 2), 20) for i in range(num_combats)]
    elif combat_type == "elite":
        rooms = [EliteRoom(createPlayer(controller=controller, cards=[], lib_path=library_path), 1, 0, [], [], random.randint(1, 2), 20) for i in range(num_combats)]
    else:
        rooms = []
    for room in rooms:
        cards = get_default_deck()
        # cards.remove("Defend")
        # cards.remove("Defend")
        # cards.extend(["Prostrate", "Worship", "EmptyBody", "CutThroughFate", "FollowUp", "JustLucky", "MentalFortress", "Wallop", "Tranquility", "Crescendo"])
        addCards(room.player, cards)

        room.player.add_relic(PureWater(room.player))

        if combat_type == "monster":
            # enemy_choice = random.choice(list(possible_enemies.keys()))
            enemy_choice = "JawWorm"
            try:
                enemy_ = getattr(possible_enemies[enemy_choice], enemy_choice)
                room.enemies = [enemy_(ascension=20, act=1)]
                room.enemies[0].health = 1
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
            room.player.deck.hand.clear()
            cards = [Defend(room.player), Defend(room.player), Defend(room.player), Defend(room.player), Strike(room.player)]
            room.player.deck.hand.extend(cards)
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

        if i % 2500 == 0: # every 100 episodes we output embedding visualizations
            print(f"Episode {i+1} complete")
            print(f"Win rate: {num_wins / (i+1)}")
            room.player.deck.reshuffle()
            deck = room.player.deck.get_deck()
            card_names = [c.name for c in deck]
            card_vectors = [controller.get_card_vector(c) for c in deck]

            controller.agent.graph_embeddings(card_names, card_vectors)

            controller.agent.save_models(f"artifacts/models/first_fight/ppo_agent.pt")

    print(f"Win rate: {num_wins / num_combats}")
    for key in sorted(enemy_combats.keys()):
        print(f"{key}: {enemy_combats[key]}")
    return enemy_combats

