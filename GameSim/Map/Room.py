import pygame

from CombatSim.Entities.Player import Player


class Room:
    def __init__(self, player: Player, type, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        self.player = player
        self.type = type
        self.prev_rooms = prev_rooms
        self.next_rooms = next_rooms
        self.act = act
        self.ascension = ascension

        self.x = x
        self.floor = floor

        # render attributes
        self.color = (100, 100, 100) # Grey

    def add_prev_room(self, room):
        # check if room is list of rooms
        if isinstance(room, list):
            for r in room:
                self.add_prev_room(r)
            return
        if room not in self.prev_rooms:
            self.prev_rooms.append(room)

    def add_next_room(self, room):
        # check if room is list of rooms
        if isinstance(room, list):
            for r in room:
                self.add_next_room(r)
            return
        if room not in self.next_rooms:
            self.next_rooms.append(room)

    def set_room_properties(self, old_room):
        # self.prev_rooms.extend(old_room.prev_rooms)
        # self.next_rooms.extend(old_room.next_rooms)
        self.prev_rooms = old_room.prev_rooms
        self.next_rooms = old_room.next_rooms
        self.x = old_room.x
        self.floor = old_room.floor

        for prev_room in self.prev_rooms:
            for next_room in prev_room.next_rooms:
                if next_room.x == self.x:
                    prev_room.next_rooms.remove(next_room)
                    prev_room.next_rooms.append(self)

        for next_room in self.next_rooms:
            for prev_room in next_room.prev_rooms:
                if prev_room.x == self.x:
                    next_room.prev_rooms.remove(prev_room)
                    next_room.prev_rooms.append(self)

    def render_map(self, screen, font, x, y, counter, tile_size, available: bool):
        if available:
            pygame.draw.rect(screen, self.color, (x-counter//24, y-counter//24, tile_size + counter // 12, tile_size + counter // 12))
        else:
            pygame.draw.rect(screen, self.color, (x, y, tile_size, tile_size))
        text = font.render(self.type, True, (0, 0, 0))
        screen.blit(text, (x + 5, y + 5))

    def render_room(self, screen, screen_size, font, render_type):
        pass

    def start(self):
        pass

    def handle_event(self, event):
        pass

    def __str__(self):
        return self.type