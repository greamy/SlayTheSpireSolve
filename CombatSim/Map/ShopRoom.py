import pygame

from CombatSim.Map.Room import Room


class ShopRoom(Room):

    def __init__(self, floor: int, x: int, prev_rooms: list, next_rooms: list):
        super().__init__("S", floor, x, prev_rooms, next_rooms)
        self.num_cards = 5
        self.num_colorless = 2
        self.num_relics = 3
        self.num_potions = 3
        self.remove_card_available = True

        # render attributes:
        self.color = (255, 0, 0) #

    # def __init__(self, room: Room):
    #     super().__init__("S", room.floor, room.x, room.prev_rooms, room.next_rooms)
    #     self.num_cards = 5
    #     self.num_colorless = 2
    #     self.num_relics = 3
    #     self.num_potions = 3
    #     self.remove_card_available = True
    #
    #     # render attributes:
    #     self.color = (255, 0, 0)  #

    def render_map(self, screen, font, x, y, counter, tile_size):
        pygame.draw.rect(screen, self.color, (x, y, tile_size, tile_size))
        text = font.render(self.type, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))
