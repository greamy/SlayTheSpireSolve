import importlib
import random
import os

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
from GameSim.Map.NewCombatRoom import NewCombatRoom
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
    plt.close(fig)

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
        # Ensure directory exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
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
    plt.close(fig)


def run_many_games(controller, dungeon_path, library_path, render_type=Renderer.RenderType.NONE, combat_type="monster", num_combats=5000, monster_name="JawWorm", cards=None):
    renderer = Renderer(render_type=render_type)

    possible_enemies = Enemy.get_implemented_enemies(dungeon_path)
    # print(possible_enemies)

    random.seed(42)
    # Use deque for wins to prevent unbounded memory growth
    # Keep only last 1000 results for rolling win rate calculation
    from collections import deque
    import gc
    wins = deque(maxlen=1000)
    total_wins = 0  # Track total wins separately
    total_combats = 0  # Track total combats
    enemy_combats = {}


    for i in range(num_combats):
        # Create a fresh room for this combat
        if combat_type == "monster":
            room = MonsterRoom(createPlayer(controller=controller, cards=[], lib_path=library_path),
                             1, 0, [], [], random.randint(1, 2), 20)
        elif combat_type == "elite":
            room = EliteRoom(createPlayer(controller=controller, cards=[], lib_path=library_path),
                           1, 0, [], [], random.randint(1, 2), 20)
        else:
            continue

        # Set up the player's deck and enemies
        if cards is None:
            cards = get_default_deck()
        addCards(room.player, cards)

        for card in room.player.deck.get_deck():
            if card.name == "Eruption":
                card.upgrade() # Upgrade one of our eruption cards.
                break

        room.player.deck.shuffle()

        if combat_type == "monster":
            enemy_choice = monster_name
            try:
                enemy_ = getattr(possible_enemies[enemy_choice], enemy_choice)
                room.enemies = [enemy_(ascension=20, act=1)]
            except AttributeError:
                room.enemies = [AcidSlimeSmall(20, 1)]
                enemy_choice = "AcidSlimeSmall"

            # Begin the combat
            room.player.controller.begin_episode()  # Reset LSTM for single-combat episode
            room.player.start_turn(room.enemies, False)
            room.player.controller.begin_combat(room.player, room.enemies, False)
        else:
            room.player.controller.begin_episode()  # Reset LSTM for single-combat episode
            room.start()
            enemy_choice = room.player.last_elite

        # Shows "NEW COMBAT" On screen when render mode is pygame.
        new_combat_room = NewCombatRoom(room.player, 0, 0, [], [], 1, 20)
        renderer.render_room(new_combat_room)

        # print(f"*********************** Fighting {enemy_choice}! {i}/{num_combats} ************************")
        renderer.render_room(room)

        total_combats += 1
        if room.player.is_alive():
            wins.append(True)
            total_wins += 1
            if enemy_choice in enemy_combats.keys():
                enemy_combats[enemy_choice][0] += 1
                enemy_combats[enemy_choice][1] += 1
            else:
                enemy_combats[enemy_choice] = [1, 1]
        else:
            wins.append(False)
            if enemy_choice in enemy_combats.keys():
                enemy_combats[enemy_choice][1] += 1
            else:
                enemy_combats[enemy_choice] = [0, 1]

        if i % 500 == 0: # every 500 episodes we output embedding visualizations
            print(f"\nCombat {i+1} complete")
            # Use rolling window for recent win rate
            print(f"Recent win rate (last {len(wins)} games): {sum(wins) / len(wins) if len(wins) > 0 else 0:.2%}")
            print(f"Overall win rate: {total_wins / total_combats:.2%}")

            # Calculate rolling stats for last 1000 combats (or fewer if less than 1000)
            window_start = max(0, len(controller.final_healths) - 1000)
            recent_healths = controller.final_healths[window_start:]
            recent_turns = controller.turn_counts[window_start:]
            recent_cards = controller.cards_played_counts[window_start:]

            # Stats for wins only in the recent window
            recent_wins = [h for h in recent_healths if h > 0]
            if recent_wins:
                recent_win_indices = [idx for idx, h in enumerate(recent_healths) if h > 0]
                avg_health_wins = sum(recent_wins) / len(recent_wins)
                avg_turns_wins = sum(recent_turns[idx] for idx in recent_win_indices) / len(recent_win_indices)
                avg_cards_wins = sum(recent_cards[idx] for idx in recent_win_indices) / len(recent_win_indices)

                print(f"Recent avg health (wins only): {avg_health_wins:.1f}")
                print(f"Recent avg turns (wins only): {avg_turns_wins:.1f}")
                print(f"Recent avg cards played (wins only): {avg_cards_wins:.1f}")

            # Overall stats for recent window
            avg_health_all = sum(recent_healths) / len(recent_healths) if recent_healths else 0
            avg_turns_all = sum(recent_turns) / len(recent_turns) if recent_turns else 0
            avg_cards_all = sum(recent_cards) / len(recent_cards) if recent_cards else 0
            print(f"Recent avg health (overall): {avg_health_all:.1f}")
            print(f"Recent avg turns (overall): {avg_turns_all:.1f}")
            print(f"Recent avg cards played (overall): {avg_cards_all:.1f}")

            # Create training progress visualization
            # Calculate rolling averages for visualization
            window = 100
            rolling_health = []
            rolling_turns = []
            rolling_cards = []
            rolling_winrate = []

            for j in range(len(controller.final_healths)):
                start_idx = max(0, j - window + 1)
                # Health (wins only)
                window_healths = controller.final_healths[start_idx:j+1]
                window_wins = [h for h in window_healths if h > 0]
                rolling_health.append(sum(window_wins) / len(window_wins) if window_wins else 0)

                # Turns (wins only)
                window_turns_all = controller.turn_counts[start_idx:j+1]
                win_turn_indices = [idx for idx, h in enumerate(window_healths) if h > 0]
                window_turns_wins = [window_turns_all[idx] for idx in win_turn_indices]
                rolling_turns.append(sum(window_turns_wins) / len(window_turns_wins) if window_turns_wins else 0)

                # Cards (wins only)
                window_cards_all = controller.cards_played_counts[start_idx:j+1]
                window_cards_wins = [window_cards_all[idx] for idx in win_turn_indices]
                rolling_cards.append(sum(window_cards_wins) / len(window_cards_wins) if window_cards_wins else 0)

                # Win rate
                rolling_winrate.append(len(window_wins) / len(window_healths) * 100 if window_healths else 0)

            # Create 2x2 subplot for training progress
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

            # Plot 1: Rolling Average Health (wins only)
            ax1.plot(rolling_health, color='tab:blue', linewidth=1, alpha=0.8)
            ax1.set_xlabel('Combat Number', fontsize=10)
            ax1.set_ylabel('Avg Health (wins)', fontsize=10)
            ax1.set_title(f'Rolling Avg Final Health (window={window}, wins only)', fontsize=12)
            ax1.grid(True, alpha=0.3)

            # Plot 2: Rolling Average Turns (wins only)
            ax2.plot(rolling_turns, color='tab:green', linewidth=1, alpha=0.8)
            ax2.set_xlabel('Combat Number', fontsize=10)
            ax2.set_ylabel('Avg Turns (wins)', fontsize=10)
            ax2.set_title(f'Rolling Avg Turns (window={window}, wins only)', fontsize=12)
            ax2.grid(True, alpha=0.3)

            # Plot 3: Rolling Average Cards Played (wins only)
            ax3.plot(rolling_cards, color='tab:orange', linewidth=1, alpha=0.8)
            ax3.set_xlabel('Combat Number', fontsize=10)
            ax3.set_ylabel('Avg Cards (wins)', fontsize=10)
            ax3.set_title(f'Rolling Avg Cards Played (window={window}, wins only)', fontsize=12)
            ax3.grid(True, alpha=0.3)

            # Plot 4: Rolling Win Rate
            ax4.plot(rolling_winrate, color='tab:purple', linewidth=1, alpha=0.8)
            ax4.set_xlabel('Combat Number', fontsize=10)
            ax4.set_ylabel('Win Rate (%)', fontsize=10)
            ax4.set_title(f'Rolling Win Rate (window={window})', fontsize=12)
            ax4.grid(True, alpha=0.3)
            ax4.set_ylim(0, 105)

            plt.tight_layout()
            plt.savefig("artifacts/images/model_results/first_fight/training_progress.png", dpi=150)
            plt.close(fig)

            room.player.deck.reshuffle()
            deck = room.player.deck.get_deck()
            card_names = [c.name for c in deck]
            card_vectors = [controller.get_card_vector(c, room.player, room.enemies) for c in deck]

            controller.agent.graph_embeddings(card_names, card_vectors)

            controller.agent.save_models(f"artifacts/models/first_fight/ppo_agent.pt")

        # Explicit garbage collection every 100 combats to prevent accumulation
        # This helps clean up numpy arrays and tensors that haven't been freed yet
        if i % 100 == 0 and i > 0:
            gc.collect()

    print(f"Final overall win rate: {total_wins / total_combats:.2%}")
    for key in sorted(enemy_combats.keys()):
        print(f"{key}: {enemy_combats[key]}")
    return enemy_combats


def run_many_game_sequences(controller, dungeon_path, library_path,
                           render_type=Renderer.RenderType.NONE,
                           num_episodes=1000,
                           combats_per_rest=3,
                           max_combats_per_episode=20,
                           heal_percent=0.20,
                           monster_name="JawWorm",
                           ascension=20,
                           act=1,
                           cards=None):
    """
    Train agent on multi-combat episodes.

    Each episode: Fight same enemy multiple times with healing between combats.
    Episode ends when player dies or max combats reached.

    Args:
        controller: RL controller
        dungeon_path: Path to enemy implementations
        library_path: Path to card library
        render_type: Rendering mode (NONE or PYGAME)
        num_episodes: Total episodes to run
        combats_per_rest: Combats between rest site bonuses (default: 4)
        max_combats_per_episode: Hard limit on combats (default: 20)
        heal_percent: HP heal between combats (default: 0.20 = 20%)
        monster_name: Enemy to fight (default: "JawWorm")
        ascension: Ascension level
        act: Act number
    """
    from collections import deque
    import gc

    renderer = Renderer(render_type=render_type)
    possible_enemies = Enemy.get_implemented_enemies(dungeon_path)

    # Episode-level statistics
    episode_wins = deque(maxlen=1000)
    total_episodes_won = 0
    combats_per_episode_history = deque(maxlen=1000)
    combats_won_per_episode_history = deque(maxlen=1000)
    health_lost_history = deque(maxlen=1000)

    random.seed(42)

    for episode_idx in range(num_episodes):
        # === EPISODE INITIALIZATION ===
        # Create Player ONCE for entire episode (not per combat!)
        player = createPlayer(controller=controller, cards=[], lib_path=library_path)
        if cards is None:
            cards = get_default_deck()

        addCards(player, cards)

        # Upgrade one Eruption
        for card in player.deck.get_deck():
            if card.name == "Eruption":
                card.upgrade()
                break

        player.deck.shuffle()

        # Episode tracking
        episode_done = False
        episode_won = False
        combats_completed = 0
        combats_won = 0
        start_health = player.health
        health_lost_per_combat = []

        # === COMBAT LOOP WITHIN EPISODE ===
        while not episode_done and combats_completed < max_combats_per_episode:
            # Create room with reused player instance
            room = MonsterRoom(player, act, 0, [], [], random.randint(1, 2), ascension)
            room.enemies = [createEnemy(monster_name, ascension, act)]

            # Combat initialization
            if combats_completed == 0:
                # First combat: initialize episode and begin combat
                controller.begin_episode()  # Resets LSTM hidden state

            # Begin combat (same for all combats - no LSTM reset in this method anymore)
            player.begin_combat(room.enemies, False)
            player.start_turn(room.enemies, False)
            controller.begin_combat(player, room.enemies, False)

            # Render combat
            new_combat_room = NewCombatRoom(player, 0, 0, [], [], 1, ascension)
            renderer.render_room(new_combat_room)
            renderer.render_room(room)

            # Store health lost
            health_lost_per_combat.append(start_health - player.health)
            start_health = player.health

            # Check combat outcome
            combat_won = player.is_alive()
            combats_completed += 1
            if combat_won:
                combats_won += 1

            # === COMBAT OUTCOME HANDLING ===
            if not player.is_alive():
                # Player died → Episode ends
                episode_done = True
                episode_won = False
                player.end_combat(room.enemies, False, episode_done=True)

            else:
                # Combat won
                # Check for rest site bonus
                if combats_completed % combats_per_rest == 0:
                    # Heal player
                    heal_amount = int(player.start_health * heal_percent)
                    player.health = min(player.health + heal_amount, player.start_health)

                    controller.apply_episode_bonus(50, reason=f"rest_site_{combats_completed // combats_per_rest}")

                # Check episode termination
                if combats_completed >= max_combats_per_episode:
                    # Reached max combats
                    episode_done = True
                    episode_won = True
                    controller.apply_episode_bonus(25, reason="max_combats_reached")
                    player.end_combat(room.enemies, False, episode_done=True)
                else:
                    # Episode continues
                    player.end_combat(room.enemies, False, episode_done=False)

        # === EPISODE STATISTICS ===
        if episode_won:
            episode_wins.append(True)
            total_episodes_won += 1
        else:
            episode_wins.append(False)

        combats_per_episode_history.append(combats_completed)
        combats_won_per_episode_history.append(combats_won)
        health_lost_history.append(sum(health_lost_per_combat) / len(health_lost_per_combat))

        # Logging
        if (episode_idx + 1) % 100 == 0:
            # Calculate rolling window averages
            recent_combats = list(combats_per_episode_history)
            recent_wins = list(combats_won_per_episode_history)
            recent_health = list(health_lost_history)

            avg_combats = np.mean(recent_combats) if recent_combats else 0
            avg_combats_won = np.mean(recent_wins) if recent_wins else 0

            # Combat win rate (total combats won / total combats played in window)
            total_combats_in_window = sum(recent_combats)
            total_wins_in_window = sum(recent_wins)
            combat_win_rate = total_wins_in_window / total_combats_in_window if total_combats_in_window > 0 else 0

            # Average health (wins only, or 0 if no wins)
            # wins_health = [h for h in recent_health if h > 0]
            avg_health = np.mean(recent_health) if recent_health else 0.0

            print(f"\n=== Episode {episode_idx+1}/{num_episodes} ===")
            print(f"Last episode: {combats_won}/{combats_completed} combats won, final health: {player.health}")
            print(f"Combat win rate (rolling): {combat_win_rate:.2%}")
            print(f"Avg combats per episode (rolling): {avg_combats:.2f}")
            print(f"Avg combats won per episode (rolling): {avg_combats_won:.2f}")
            print(f"Avg health lost per combat(rolling): {avg_health:.1f}")

        # Save model and create visualizations
        if (episode_idx + 1) % 500 == 0:
            print(f"\n{'='*60}")
            print(f"Creating visualizations at episode {episode_idx+1}...")
            print(f"{'='*60}")

            # Calculate rolling window statistics for all combats
            window = 100
            rolling_health = []
            rolling_turns = []
            rolling_cards = []
            rolling_winrate = []

            # Note: In multi-combat episodes, we track per-combat stats differently
            # We'll use the total number of completed episodes for the rolling window
            for j in range(len(controller.final_healths)):
                start_idx = max(0, j - window + 1)
                # Health lost
                window_healths = controller.final_healths[start_idx:j+1]
                window_wins = [h for h in window_healths if h > 0]
                # window_health_lost = [controller.start_health - h for idx, h in enumerate(window_healths) if h > 0]
                # rolling_health.append(sum(window_health_lost) / len(window_health_lost) if window_health_lost else 0)

                # Turns (wins only)
                window_turns_all = controller.turn_counts[start_idx:j+1]
                win_turn_indices = [idx for idx, h in enumerate(window_healths) if h > 0]
                window_turns_wins = [window_turns_all[idx] for idx in win_turn_indices]
                rolling_turns.append(sum(window_turns_wins) / len(window_turns_wins) if window_turns_wins else 0)

                # Cards (wins only)
                window_cards_all = controller.cards_played_counts[start_idx:j+1]
                window_cards_wins = [window_cards_all[idx] for idx in win_turn_indices]
                rolling_cards.append(sum(window_cards_wins) / len(window_cards_wins) if window_cards_wins else 0)

                # Win rate (episodes that didn't end in death)
                rolling_winrate.append(len(window_wins) / len(window_healths) * 100 if window_healths else 0)

            # Create 2x2 subplot for training progress
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

            # Plot 1: Rolling Average Health (wins only)
            ax1.plot(health_lost_history, color='tab:blue', linewidth=1, alpha=0.8)
            ax1.set_xlabel('Combat Number', fontsize=10)
            ax1.set_ylabel('Avg Health (wins)', fontsize=10)
            ax1.set_title(f'Rolling Avg Health Lost (window={window}, wins only)', fontsize=12)
            ax1.grid(True, alpha=0.3)

            # Plot 2: Rolling Average Turns (wins only)
            ax2.plot(rolling_turns, color='tab:green', linewidth=1, alpha=0.8)
            ax2.set_xlabel('Combat Number', fontsize=10)
            ax2.set_ylabel('Avg Turns (wins)', fontsize=10)
            ax2.set_title(f'Rolling Avg Turns per Episode (window={window}, wins only)', fontsize=12)
            ax2.grid(True, alpha=0.3)

            # Plot 3: Rolling Average Cards Played (wins only)
            ax3.plot(rolling_cards, color='tab:orange', linewidth=1, alpha=0.8)
            ax3.set_xlabel('Combat Number', fontsize=10)
            ax3.set_ylabel('Avg Cards (wins)', fontsize=10)
            ax3.set_title(f'Rolling Avg Cards Played per Episode (window={window}, wins only)', fontsize=12)
            ax3.grid(True, alpha=0.3)

            # Plot 4: Rolling Win Rate (episodes that survived)
            ax4.plot(rolling_winrate, color='tab:purple', linewidth=1, alpha=0.8)
            ax4.set_xlabel('Combat Number', fontsize=10)
            ax4.set_ylabel('Survival Rate (%)', fontsize=10)
            ax4.set_title(f'Rolling Episode Survival Rate (window={window})', fontsize=12)
            ax4.grid(True, alpha=0.3)
            ax4.set_ylim(0, 105)

            plt.tight_layout()
            plt.savefig("artifacts/images/model_results/first_fight/combat_stats.png", dpi=150)
            plt.close(fig)
            print("✓ Combat statistics graph saved")

        # Garbage collection
        if episode_idx % 100 == 0 and episode_idx > 0:
            gc.collect()

    # Final statistics
    total_combats = sum(combats_per_episode_history)
    total_combats_won = sum(combats_won_per_episode_history)
    final_combat_win_rate = total_combats_won / total_combats if total_combats > 0 else 0

    print(f"\n=== Training Complete ===")
    print(f"Total combats: {total_combats}")
    print(f"Total combats won: {total_combats_won}")
    print(f"Overall combat win rate: {final_combat_win_rate:.2%}")
    print(f"Avg combats per episode: {np.mean(combats_per_episode_history):.2f}")
    print(f"Avg combats won per episode: {np.mean(combats_won_per_episode_history):.2f}")
    print(f"Episodes that reached max combats: {total_episodes_won}/{num_episodes}")

    return {
        "combat_win_rate": final_combat_win_rate,
        "avg_combats_per_episode": np.mean(combats_per_episode_history),
        "avg_combats_won_per_episode": np.mean(combats_won_per_episode_history),
        "total_combats": total_combats,
        "total_combats_won": total_combats_won,
        "episode_win_rate": total_episodes_won / num_episodes
    }

