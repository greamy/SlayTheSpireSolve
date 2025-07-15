import pygame

from GameSim.Map.Room import Room


class ShopRoom(Room):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "S", floor, x, prev_rooms, next_rooms, act, ascension)
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

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)

    def render_room(self, screen, screen_size, font):
        pass
