import pygame

from CombatSim.Map.Room import Room


class ChestRoom(Room):

    def __init__(self, floor: int, x: int, prev_rooms: list, next_rooms: list):
        super().__init__("C", floor, x, prev_rooms, next_rooms)

        # render attributes
        self.color = (255, 215, 0) # Gold

    def render_map(self, screen, font, x, y, counter, tile_size):
        self.color = (255, 215 + (counter // 7), counter)
        pygame.draw.rect(screen, self.color, (x, y, tile_size, tile_size))
        text = font.render(self.type, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))

    def render_room(self, screen, screen_size, font):
        pass
