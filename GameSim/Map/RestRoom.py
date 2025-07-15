import pygame

from GameSim.Map.Room import Room


class RestRoom(Room):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "R", floor, x, prev_rooms, next_rooms, act, ascension)

        # render attributes
        self.color = (20, 255, 20) # Green

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font):
        img = pygame.image.load("../images/Rooms/campfire.png")
        img = pygame.transform.scale(img, screen_size, screen)
