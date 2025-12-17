import numpy as np

from GameSim.BotTraining.Regimen import Regimen
from GameSim.Input import Controller
from GameSim.Input.RLPlayerController import RLPlayerController
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, addCards, get_default_deck

class Trainer:

    def __init__(self, renderer: Renderer, agent_save_path="artifacts/images/model_results/first_fight/"):
        self.renderer = renderer
        self.controller = RLPlayerController(agent_save_path, delay=0, train=True)
        # self.player = self.get_player(self.controller)

        self.act = 1
        self.ascension = 20

        self.curriculum: list[Regimen] = []

    def add_regimen(self, regimen: Regimen):
        self.curriculum.append(regimen)

    def run(self):
        for reg in self.curriculum:
            rooms = reg.get_rooms(self.controller)

            start_health = self.controller.start_health
            health_lost_per_combat = []

            for idx, room in enumerate(rooms):
                self.controller.begin_episode()
                self.renderer.render_room(room)

                # TODO: Collect reward logs and generate graphs if needed
                health_lost_per_combat.append(start_health - max(reg.player.health, 0))

                window = 1000
                if (idx+1) % 100 == 0:
                    # Calculate rolling window averages
                    recent_combats = self.controller.combats_per_episode[-window:]
                    recent_wins = self.controller.wins_per_episode[-window:]
                    recent_health = health_lost_per_combat

                    avg_combats = np.mean(recent_combats) if recent_combats else 0
                    avg_combats_won = np.mean(recent_wins) if recent_wins else 0

                    # Combat win rate (total combats won / total combats played in window)
                    total_combats_in_window = sum(recent_combats)
                    total_wins_in_window = sum(recent_wins)
                    combat_win_rate = total_wins_in_window / total_combats_in_window if total_combats_in_window > 0 else 0

                    # Average health (wins only, or 0 if no wins)
                    # wins_health = [h for h in recent_health if h > 0]
                    avg_health = np.mean(recent_health) if recent_health else 0.0

                    print(f"\n=== Episode {idx + 1}/{reg.max_episodes} ===")
                    print(f"Combat win rate (rolling): {combat_win_rate:.2%}")
                    print(f"Avg combats per episode (rolling): {avg_combats:.2f}")
                    print(f"Avg combats won per episode (rolling): {avg_combats_won:.2f}")
                    print(f"Avg health lost per combat(rolling): {avg_health:.1f}")
                # TODO: implement early-stopping somehow to stop running episodes if reward has stagnated
            self.controller.save_agent("artifacts/models/first_fight/ppo_agent_"+ str(idx) +".pt")

