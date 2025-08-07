import importlib
import random

import pygame
import copy

from CombatSim.Entities.Dungeon.GremlinNob import GremlinNob
from CombatSim.Entities.Enemy import Enemy
from GameSim.Map.CombatRoom import CombatRoom
from GameSim.Map.Room import Room


class EliteRoom(CombatRoom):

    ELITES = {
        1: ["GremlinNob", "Lagavulin", "Sentry"],
        # 1: ["GremlinNob", "Lagavulin"],
        # 2: ["GremlinLeader", "BookofStabbing", "Slavers"],
        2: [ "Taskmaster"],
        3: ["GiantHead", "Repomancer", "Nemesis"],
    }

    MULTI_COMBATS = {
        "Sentry": ["Sentry", "Sentry", "Sentry"],
        "Taskmaster": ["BlueSlaver", "Taskmaster", "RedSlaver"]
    }

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "E", floor, x, prev_rooms, next_rooms, act, ascension)

        # render attributes:
        self.color = (255, 0, 0)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        self.color = (255, min(counter, 200), 0)
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def create_enemies(self, act, ascension) -> list[Enemy]:
        last_elite = self.player.last_elite
        list_of_act_elites = self.ELITES[act]
        if last_elite is not None:
            # choose from remaining elites
            list_of_act_elites = [elite for elite in list_of_act_elites if elite != last_elite]

        elite_name = random.choice(list_of_act_elites)
        if elite_name in self.MULTI_COMBATS.keys():
            enemies = []
            for name in self.MULTI_COMBATS[elite_name]:
                module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
                class_ = getattr(module, name)
                enemies.append(class_(ascension, act))
            return enemies
        module = importlib.import_module("CombatSim.Entities.Dungeon." + elite_name)
        class_ = getattr(module, elite_name)
        return [class_(ascension, act)]

    def start(self):
        super().start()
        self.player.last_elite = self.enemies[0].__class__.__name__

    # def render_room(self, screen, screen_size, font):
    #     pass
