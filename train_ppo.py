import matplotlib

from GameSim.Input.RandomPlayerController import RandomPlayerController
from GameSim.Render.Renderer import Renderer

matplotlib.use('Agg')
from matplotlib import pyplot as plt

from GameSim.Input.RLPlayerController import RLPlayerController
from CombatSim.util import run_many_games


def main():
    episodes = 50_000
    rl_controller = RLPlayerController(delay=2, train=False, filepath="artifacts/images/model_results/first_fight/")
    # rl_controller = RandomPlayerController(delay=0)
    rl_controller.agent.load_models(f"artifacts/models/first_fight/ppo_agent_{episodes}.pt")
    # rl_controller.agent.load_models(f"artifacts/models/first_fight/best_lstm_first_fight.pt")
    run_many_games(rl_controller, "CombatSim/Entities/Dungeon/", "CombatSim/Actions/Library",
                   Renderer.RenderType.PYGAME, "monster", episodes)

    rl_controller.agent.save_models(f"artifacts/models/first_fight/ppo_agent_{episodes}.pt")

    plt.plot(rl_controller.final_healths, color='tab:blue', marker='x', linestyle='-', label='Average Reward')
    plt.xlabel('Learning Period', fontsize=12)
    plt.ylabel('Final Health', fontsize=12)
    plt.title('Final health from fight over time', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()

    plt.savefig("artifacts/images/model_results/first_fight/final_healths.png")


if __name__ == "__main__":
    main()

