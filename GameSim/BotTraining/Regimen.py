import importlib
import random
from copy import copy, deepcopy
from typing import Generator

import numpy as np
from pygame._sdl2 import controller

from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Enemy import Enemy
from CombatSim.util import createPlayer, addCards, get_default_deck
from GameSim.Map.MonsterRoom import MonsterRoom


class Regimen:

    def __init__(self, max_episodes: int, possible_enemies: list[str], num_enemies: int|list[int], default_deck: list[str],
                 num_additional_cards: int = 0, additional_cards: dict = None, allow_repeat_enemies=True, player_max_health=70, player_start_health=70,
                 rest_freq=4, max_gauntlet_length=20, dungeon_path="CombatSim/Entities/Dungeon/", library_path="CombatSim/Actions/Library"):
        self.max_episodes = max_episodes
        self.possible_enemies = possible_enemies
        self.default_deck = default_deck
        self.additional_cards = additional_cards
        self.player_max_health = player_max_health
        self.player_start_health = player_start_health
        self.num_enemies = num_enemies
        self.num_additional_cards = num_additional_cards
        self.allow_repeat_enemies = allow_repeat_enemies
        self.rest_frequency = rest_freq
        self.max_gauntlet_length = max_gauntlet_length
        self.dungeon_path = dungeon_path
        self.library_path = library_path


    def get_player(self, controller):
        player = createPlayer(controller=controller, health=self.player_start_health, cards=self._get_deck_list(),
                              max_health=self.player_max_health, lib_path=self.library_path)

        return player

    def _get_deck_list(self):
        deck = self.default_deck
        additions = []
        if self.additional_cards is not None and self.num_additional_cards is not None:
            additions.extend(np.random.choice(a=list(self.additional_cards.keys()), size=self.num_additional_cards, p=list(self.additional_cards.values())))
        deck = deck + additions
        return deck

    def _get_enemies(self):
        implemented_enemies = Enemy.get_implemented_enemies(self.dungeon_path)
        enemies = []
        allowed_enemies = deepcopy(self.possible_enemies)
        enemy_number = self.num_enemies
        if isinstance(self.num_enemies, list):
            enemy_number = random.choice(self.num_enemies)
        for _ in range(enemy_number):
            enemy_choice = random.choice(allowed_enemies)
            if not self.allow_repeat_enemies:
                allowed_enemies.remove(enemy_choice)
            if isinstance(enemy_choice, list):
                enemies = []
                for name in enemy_choice:
                    module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
                    class_ = getattr(module, name)
                    enemies.append(class_(ascension=20, act=1))
                return enemies
            else:
                try:
                    enemy_ = getattr(implemented_enemies[enemy_choice], enemy_choice)
                    enemies.append(enemy_(ascension=20, act=1))
                except AttributeError:
                    enemies = [AcidSlimeSmall(20, 1)]
        return enemies

    # returns a generator that yields rooms for the regimen
    def get_rooms(self, controller) -> Generator[MonsterRoom, None, None]:
        episodes = 0

        current_combat = 0
        self.player = self.get_player(controller)
        enemies = self._get_enemies()
        while episodes < self.max_episodes:
            if not self.player.is_alive() or current_combat > self.max_gauntlet_length:
                self.player = self.get_player(controller)
                current_combat = 0
            elif current_combat > 1:
                self.player.end_combat(enemies, False, episode_done=False)
            room = MonsterRoom(self.player,1, 0, [], [], 1, 20)
            enemies = self._get_enemies()
            room.enemies = enemies

            if episodes % self.rest_frequency == 0 and episodes != 0:
                self.player.health = max(self.player.health + int(self.player.start_health * 0.2), self.player.start_health)

            episodes += 1
            current_combat += 1
            yield room
        print("Regimen completed all episodes. Moving to next regimen if available.")
