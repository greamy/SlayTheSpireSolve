import pygame

from GameSim.Map.Room import Room


class EventRoom(Room):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player,"?", floor, x, prev_rooms, next_rooms, act, ascension)
        # TODO: Choose event type or trust external class to do it.
        self.event_types = None
        # render attributes
        self.color = (0, 255, 255)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font):
        pass
