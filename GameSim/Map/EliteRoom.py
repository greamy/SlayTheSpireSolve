import pygame

from GameSim.Map.Room import Room


class EliteRoom(Room):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "E", floor, x, prev_rooms, next_rooms, act, ascension)
        # TODO: Choose elite monster somehow... or trust external class (combat class perhaps) to choose one for us.
        self.monster = None

        # render attributes:
        self.color = (255, 0, 0)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        self.color = (255, min(counter, 200), 0)
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font):
        pass
