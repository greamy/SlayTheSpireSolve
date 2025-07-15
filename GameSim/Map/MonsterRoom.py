import pygame

from GameSim.Map.CombatRoom import CombatRoom
from CombatSim.Entities.Dungeon.JawWorm import JawWorm
from GameSim.Map.Room import Room


class MonsterRoom(CombatRoom):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "M", floor, x, prev_rooms, next_rooms, act, ascension)
        # TODO: Choose elite monster somehow... or trust external class (combat class perhaps) to choose one for us.
        # self.monster = JawWorm(1, 1)
        # self.combat = None
        # render attributes
        self.color = (175, 125, 0) # Brown

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)
