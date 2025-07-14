import pygame

from CombatSim.Map.Room import Room


class EliteRoom(Room):

    def __init__(self, floor: int, x: int, prev_rooms: list, next_rooms: list):
        super().__init__("E", floor, x, prev_rooms, next_rooms)
        # TODO: Choose elite monster somehow... or trust external class (combat class perhaps) to choose one for us.
        self.monster = None

        # render attributes:
        self.color = (255, 0, 0)

    def render_map(self, screen, font, x, y, counter, tile_size):
        self.color = (255, min(counter, 200), 0)
        pygame.draw.rect(screen, self.color, (x, y, tile_size, tile_size))
        text = font.render(self.type, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))
