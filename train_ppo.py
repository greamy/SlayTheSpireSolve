import matplotlib

from GameSim.Input.RandomPlayerController import RandomPlayerController
from GameSim.Render.Renderer import Renderer

matplotlib.use('Agg')
from matplotlib import pyplot as plt

from GameSim.Input.RLPlayerController import RLPlayerController
from CombatSim.util import run_many_games, run_many_game_sequences


def main():
    """
    PPO Training/Benchmarking Script

    Configuration:
    - For TRAINING: set train=True, delay=0, render_type=NONE, episodes=large number (e.g., 250_000)
    - For BENCHMARKING: set train=False, delay=0, render_type=NONE, episodes=benchmark size (e.g., 1000)
    - For VISUALIZATION: set delay=3, render_type=PYGAME (slow)

    The script will output:
    - Win rate
    - Average health remaining (wins only and overall)
    - Average turns per combat (wins only and overall)
    - Average cards played per combat (wins only and overall)
    - Visualization graphs saved to artifacts/images/model_results/first_fight/combat_stats.png
    """

    # Configuration
    episodes = 1000
    train = False
    delay = 0
    render_type = Renderer.RenderType.NONE
    load_model = True
    model_path = "artifacts/models/first_fight/ppo_agent_JawWormMulti.pt"

    rl_controller = RLPlayerController(delay=delay, train=train, filepath="artifacts/images/model_results/first_fight/")
    if load_model:
        rl_controller.agent.load_models(model_path)

    run_many_games(rl_controller, "CombatSim/Entities/Dungeon/", "CombatSim/Actions/Library",
                   render_type, "monster", episodes, "JawWorm")

    # run_many_game_sequences(
    #     controller=rl_controller,
    #     dungeon_path="CombatSim/Entities/Dungeon/",
    #     library_path="CombatSim/Actions/Library",
    #     num_episodes=episodes,  # Total episodes to run
    #     combats_per_rest=4,  # Rest bonus every N combats
    #     max_combats_per_episode=20,  # Hard cap
    #     heal_percent=0.20,  # 20% heal between combats
    #     monster_name="JawWorm",  # Enemy to fight
    #     ascension=20,
    #     act=1
    # )

    if train:
        rl_controller.agent.save_models(f"artifacts/models/first_fight/ppo_agent_{episodes}.pt")

    # Calculate and print statistics
    print("\n" + "="*50)
    print("COMBAT STATISTICS")
    print("="*50)

    # Filter out losses (health <= 0) for win-only stats
    wins = [h for h in rl_controller.final_healths if h > 0]
    win_indices = [i for i, h in enumerate(rl_controller.final_healths) if h > 0]

    print(f"Total Combats: {len(rl_controller.final_healths)}")
    print(f"Wins: {len(wins)}")
    print(f"Win Rate: {len(wins)/len(rl_controller.final_healths)*100:.2f}%")
    print()

    if wins:
        avg_health = sum(wins) / len(wins)
        print(f"Average Health Remaining (wins only): {avg_health:.2f}")

        win_turns = [rl_controller.turn_counts[i] for i in win_indices]
        avg_turns = sum(win_turns) / len(win_turns)
        print(f"Average Turns per Combat (wins only): {avg_turns:.2f}")

        win_cards = [rl_controller.cards_played_counts[i] for i in win_indices]
        avg_cards = sum(win_cards) / len(win_cards)
        print(f"Average Cards Played per Combat (wins only): {avg_cards:.2f}")

    # Overall stats (including losses)
    print()
    print("Overall Stats (including losses):")
    avg_health_all = sum(rl_controller.final_healths) / len(rl_controller.final_healths)
    print(f"Average Final Health: {avg_health_all:.2f}")

    avg_turns_all = sum(rl_controller.turn_counts) / len(rl_controller.turn_counts)
    print(f"Average Turns per Combat: {avg_turns_all:.2f}")

    avg_cards_all = sum(rl_controller.cards_played_counts) / len(rl_controller.cards_played_counts)
    print(f"Average Cards Played per Combat: {avg_cards_all:.2f}")
    print("="*50 + "\n")

    # Create visualizations
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Final Health
    ax1.plot(rl_controller.final_healths, color='tab:blue', marker='', linestyle='-', linewidth=0.5, alpha=0.7)
    ax1.set_xlabel('Combat Number', fontsize=10)
    ax1.set_ylabel('Final Health', fontsize=10)
    ax1.set_title('Final Health per Combat', fontsize=12)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)

    # Plot 2: Turns per Combat
    ax2.plot(rl_controller.turn_counts, color='tab:green', marker='', linestyle='-', linewidth=0.5, alpha=0.7)
    ax2.set_xlabel('Combat Number', fontsize=10)
    ax2.set_ylabel('Turns', fontsize=10)
    ax2.set_title('Turns per Combat', fontsize=12)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)

    # Plot 3: Cards Played per Combat
    ax3.plot(rl_controller.cards_played_counts, color='tab:orange', marker='', linestyle='-', linewidth=0.5, alpha=0.7)
    ax3.set_xlabel('Combat Number', fontsize=10)
    ax3.set_ylabel('Cards Played', fontsize=10)
    ax3.set_title('Cards Played per Combat', fontsize=12)
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)

    # Plot 4: Win Rate (rolling average over 100 games)
    window_size = min(100, len(rl_controller.final_healths))
    win_rate_rolling = []
    for i in range(len(rl_controller.final_healths)):
        start = max(0, i - window_size + 1)
        window = rl_controller.final_healths[start:i+1]
        win_rate = sum(1 for h in window if h > 0) / len(window) * 100
        win_rate_rolling.append(win_rate)

    ax4.plot(win_rate_rolling, color='tab:purple', marker='', linestyle='-', linewidth=0.5, alpha=0.7)
    ax4.set_xlabel('Combat Number', fontsize=10)
    ax4.set_ylabel('Win Rate (%)', fontsize=10)
    ax4.set_title(f'Rolling Win Rate (window={window_size})', fontsize=12)
    ax4.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
    ax4.set_ylim(0, 105)

    plt.tight_layout()
    plt.savefig("artifacts/images/model_results/first_fight/combat_stats.png", dpi=150)
    plt.close(fig)
    print(f"Visualizations saved to artifacts/images/model_results/first_fight/combat_stats.png")


if __name__ == "__main__":
    main()

