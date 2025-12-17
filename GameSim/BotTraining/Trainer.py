import numpy as np

from GameSim.BotTraining.Regimen import Regimen
from GameSim.Input import Controller
from GameSim.Input.RLPlayerController import RLPlayerController
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, addCards, get_default_deck

class Trainer:

    def __init__(self, renderer: Renderer, agent_save_path="artifacts/images/model_results/first_fight/", train=True, save=True, delay=0):
        self.renderer = renderer
        self.controller = RLPlayerController(agent_save_path, delay=delay, train=train, save=save)
        # self.player = self.get_player(self.controller)
        self.save = save
        self.train = train

        self.act = 1
        self.ascension = 20

        self.curriculum: list[Regimen] = []

    def add_regimen(self, regimen: Regimen):
        self.curriculum.append(regimen)

    def run(self):
        for reg in self.curriculum:
            rooms = reg.get_rooms(self.controller)

            health_lost_per_combat = []

            # Track gauntlet state
            current_gauntlet_combats = 0
            gauntlet_active = False
            previous_player = None

            for idx, room in enumerate(rooms):
                # Check if this is a new gauntlet (new player instance)
                is_new_gauntlet = (room.player != previous_player)

                if is_new_gauntlet:
                    # New gauntlet starting - reset LSTM and begin episode
                    self.controller.begin_episode()
                    current_gauntlet_combats = 0
                    gauntlet_active = True
                    previous_player = room.player

                # Store player health before combat
                health_before = room.player.health

                # Execute the combat
                self.renderer.render_room(room)

                # Increment gauntlet combat counter
                current_gauntlet_combats += 1

                # Check combat outcome
                combat_won = room.player.is_alive()

                # Determine if gauntlet/episode ends after this combat
                gauntlet_ends = (
                    not combat_won or  # Player died
                    current_gauntlet_combats >= reg.max_gauntlet_length  # Reached max length
                )

                # Call end_combat with appropriate episode_done flag
                if gauntlet_active:
                    room.player.end_combat(room.enemies, False, episode_done=gauntlet_ends)

                    # Apply rest site healing and bonus if applicable (based on gauntlet combat count)
                    # Only apply if episode continues and we hit a rest milestone
                    if not gauntlet_ends and current_gauntlet_combats % reg.rest_frequency == 0:
                        # Heal the player
                        heal_amount = int(room.player.start_health * 0.20)
                        room.player.health = min(room.player.health + heal_amount, room.player.start_health)
                        # Apply bonus reward
                        self.controller.apply_episode_bonus(50, reason=f"rest_site")

                    # Apply max gauntlet bonus if reached max length
                    if gauntlet_ends and combat_won and current_gauntlet_combats >= reg.max_gauntlet_length:
                        self.controller.apply_episode_bonus(25, reason="max_combats_reached")

                    if gauntlet_ends:
                        gauntlet_active = False

                # Track health lost this combat
                health_lost_per_combat.append(max(health_before - room.player.health, 0))
                self.log_room(idx, health_lost_per_combat, reg.max_episodes)

    def log_room(self, idx, health_lost_per_combat, max_episodes):

        # Logging
        window = 1000
        if (idx+1) % 100 == 0:
            # Calculate rolling window averages
            recent_combats = self.controller.combats_per_episode[-window:]
            recent_wins = self.controller.wins_per_episode[-window:]
            recent_health = health_lost_per_combat[-window:]

            avg_combats = np.mean(recent_combats) if recent_combats else 0
            avg_combats_won = np.mean(recent_wins) if recent_wins else 0

            # Combat win rate (total combats won / total combats played in window)
            total_combats_in_window = sum(recent_combats)
            total_wins_in_window = sum(recent_wins)
            combat_win_rate = total_wins_in_window / total_combats_in_window if total_combats_in_window > 0 else 0

            # Average health lost per combat
            avg_health = np.mean(recent_health) if recent_health else 0.0

            print(f"\n=== Episode {idx + 1}/{max_episodes} ===")
            print(f"Combat win rate (rolling): {combat_win_rate:.2%}")
            print(f"Avg combats per episode (rolling): {avg_combats:.2f}")
            print(f"Avg combats won per episode (rolling): {avg_combats_won:.2f}")
            print(f"Avg health lost per combat (rolling): {avg_health:.1f}")

        # Save model periodically
        if self.save and (idx+1) % 20_000 == 0:
            self.controller.save_agent(f"artifacts/models/first_fight/ppo_agent_{idx+1}.pt")


