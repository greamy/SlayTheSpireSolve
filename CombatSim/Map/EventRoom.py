import pygame

from CombatSim.Map.Room import Room


class EventRoom(Room):

    def __init__(self, floor: int, x: int, prev_rooms: list, next_rooms: list):
        super().__init__("?", floor, x, prev_rooms, next_rooms)
        # TODO: Choose event type or trust external class to do it.
        self.event_types = None
        # render attributes
        self.color = (0, 255, 255)

    def render_map(self, screen, font, x, y, counter, tile_size):
        pygame.draw.rect(screen, self.color, (x, y, tile_size, tile_size))
        text = font.render(self.type, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))

    def render_room(self, screen, screen_size, font):
        pass
