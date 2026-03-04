import copy
import os
import random

import numpy as np

from GameSim.BotTraining.Regimen import Regimen
from GameSim.Input import Controller
from GameSim.Input.RLPlayerController import RLPlayerController
from GameSim.Map.Map import Map
from GameSim.Map.MapGenerator import MapGenerator
from GameSim.Render.Renderer import Renderer

from CombatSim.util import createPlayer, addCards, get_default_deck

class TrainerFullAct:

    def __init__(self, episodes: int, renderer: Renderer, agent_save_path="artifacts/images/model_results/first_fight/", train=True, save=True, delay=0,
                 combat_sim_path="CombatSim/", visualizer=None):
        self.episodes = episodes
        self.renderer = renderer
        self.visualizer = visualizer
        self.controller = RLPlayerController(agent_save_path, delay=delay, train=train, save=save, visualizer=visualizer)
        # self.player = self.get_player(self.controller)
        self.save = save
        self.train = train

        self.act = 1
        self.ascension = 20

        self.player_start_health = 70
        self.player_max_health = 70
        self.library_path = os.path.join(combat_sim_path, "Actions/Library")
        self.relic_path = os.path.join(combat_sim_path, "Items/Relics/DisplayCase")
        self.dungeon_path = os.path.join(combat_sim_path, "Entities/Dungeon")

        self.player = self.get_player(self.controller)
        self.map_gen = MapGenerator(self.player, self.act, self.ascension)
        self.cur_map = self.map_gen.generate_map()

        self.random_floor_chance = 0.4

    def get_player(self, controller):
        player = createPlayer(controller=controller, health=self.player_start_health, cards=get_default_deck(),
                              max_health=self.player_max_health, lib_path=self.library_path, relic_path=self.relic_path)
        return player

    def reset_episode(self):
        new_player = self.get_player(self.controller)
        self.map_gen.player = new_player
        self.cur_map = self.map_gen.generate_map()

        # randomize starting floor based on self.random_floor_chance
        # if np.random.rand() < self.random_floor_chance:
        if False:
            random_floor = np.random.randint(2, self.cur_map.grid_y-2)
            available_rooms = self.cur_map.get_avail_floors(random_floor, None)
            random_room = np.random.choice(available_rooms)
            self.cur_map.player_pos = (random_floor, random_room)

            # give player randomly selected good cards based on current floor:
            additional_cards = []
            additional_relics = []
            if random_floor < 5:
                # early floors 2-5
                additional_cards += ["Eruption", "Vigilance", "BattleHymn"]
                additional_relics += ["BurningBlood", "Vajra", "ToxicEgg"]
            elif random_floor < 10:
                # mid floors 6-10
                additional_cards += ["CutThroughFate", "BowlingBash", "FollowUp", "TalktotheHand", "CarveReality", "Brilliance"]
                additional_relics += ["BlackBlood", "Shuriken", "Orichalcum"]
            else:
                # later floors 11-15
                additional_cards += ["FlurryofBlows", "Tantrum", "ReachHeaven", "Rushdown"]
                additional_relics += ["Ginger", "MeatOnTheBone", "RunicPyramid"]
            # random additional cards and relics within range of possible values
            num_additional_cards = random.randint(random_floor-2, random_floor)
            num_additional_relics = random.randint(0, random_floor // 3)
            additional_cards = np.random.choice(additional_cards, size=num_additional_cards, replace=False)
            addCards(new_player, additional_cards)

            additional_relics = np.random.choice(additional_relics, size=num_additional_relics, replace=False)
            for relic_name in additional_relics:
                if relic_name in new_player.implemented_relics:
                    cls = getattr(new_player.implemented_relics[relic_name], relic_name)
                    new_player.add_relic(cls(new_player))

    def run(self):
        for episode in range(self.episodes):
            self.reset_episode()
            self.controller.begin_episode()
            health_lost_per_combat = []
            combats_this_episode = 0
            combats_won_this_episode = 0

            next_room = self.renderer.render_act_map(self.cur_map, self.cur_map.player_pos[0], self.cur_map.player_pos[1])
            while next_room:
                room = next_room
                health_before = room.player.health

                self.renderer.render_room(room)
                self.cur_map.player_pos = (room.floor + 1, room.x)

                next_room = self.renderer.render_act_map(self.cur_map, self.cur_map.player_pos[0],
                                                         self.cur_map.player_pos[1])
                episode_done = next_room is None

                combat_won = room.player.is_alive()
                health_lost_per_combat.append(max(health_before - room.player.health, 0))
                combats_this_episode += 1
                if combat_won:
                    combats_won_this_episode += 1

                if not combat_won:
                    room.player.end_combat(room.enemies, False, episode_done=True)
                    break
                else:
                    room.player.end_combat(room.enemies, False, episode_done=episode_done)

            if self.visualizer:
                self.visualizer.log_episode(
                    combats=combats_this_episode,
                    combats_won=combats_won_this_episode,
                    episode=episode
                )

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
