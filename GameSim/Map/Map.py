import pygame

from GameSim.Map.Room import Room


class Map:
    ROOM_TYPE_CHEST = 'C'
    ROOM_TYPE_ELITE = 'E'
    ROOM_TYPE_EVENT = '?'
    ROOM_TYPE_MONSTER = 'M'
    ROOM_TYPE_REST = 'R'
    ROOM_TYPE_SHOP = 'S'
    ROOM_TYPE_UNSET = 'P' # Node in a path that has not been set to a room type

    def __init__(self, player, act, ascension, generated_map: list):
        self.grid_x = 7
        self.grid_y = 15
        self.num_paths = 6
        self.map = generated_map

        self.player = player
        self.act = act
        self.ascension = ascension

        self.player_pos: tuple = (0, None) # (floor, room_idx) - floor is 0 indexed, room_idx is None if not set yet

        # rendering attributes:
        self.tile_size = 30
        self.tile_spacing = 15
        self.x_align = 650 - (self.grid_x * self.tile_size + (self.grid_x - 1) * self.tile_spacing)
        self.counter = 0
        self.counter_up = True

    def calculate_position_from_idx(self, floor_idx, room_idx, screen_size=(1280, 720)):
        return (self.x_align + room_idx * self.tile_size + room_idx * self.tile_spacing * 2,
                (screen_size[1] - self.tile_size - self.tile_spacing) - (
                            floor_idx * self.tile_size + floor_idx * self.tile_spacing))

    def get_avail_floors(self, floor, room_idx) -> list[int]:
        if room_idx is None:
            avail_floors = self.map[floor]
            avail_floors = [floor.x for floor in avail_floors if floor is not None]
        else:
            cur_room = self.map[floor - 1][room_idx]
            avail_floors = cur_room.next_rooms
        return list(avail_floors)

    def render(self, screen, screen_size, font, cur_floor, room_idx, render_type):
        color_map = {
            self.ROOM_TYPE_CHEST: (255, 215 + (self.counter // 7), self.counter),  # Gold
            self.ROOM_TYPE_ELITE: (255, min(self.counter, 200), 0),    # Red
            self.ROOM_TYPE_EVENT: (0, 255, 255),  # Cyan
            self.ROOM_TYPE_MONSTER: (175, 125, 0), # Red
            self.ROOM_TYPE_REST: 'green',     # green
            self.ROOM_TYPE_SHOP: (255, 0, 0),     # Purple
            self.ROOM_TYPE_UNSET: (100, 100, 100) # White
        }
        counter_amt = 6
        if self.counter_up and self.counter == 255:
            self.counter_up = False
        elif not self.counter_up and self.counter <= 0:
            self.counter_up = True
        else:
            self.counter += counter_amt if self.counter_up else -counter_amt
            if self.counter > 255:
                self.counter = 255
            elif self.counter < 0:
                self.counter = 0

        avail_floors = self.get_avail_floors(cur_floor, room_idx)
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                room = self.map[y][x]
                if room is not None:
                    x_pos, y_pos = self.calculate_position_from_idx(y, x, screen_size)

                    room.render_map(screen, font, x_pos, y_pos, self.counter, self.tile_size,
                                    (room.floor == cur_floor and room.x in avail_floors))

                    prev_room_idxs = room.prev_rooms

                    for prev_room_idx in prev_room_idxs:
                        x_pos, y_pos = self.calculate_position_from_idx(y, x, screen_size)
                        if prev_room_idx is None:
                            continue
                        prev_x, prev_y = self.calculate_position_from_idx(y-1, prev_room_idx, screen_size)
                        if prev_room_idx == x:
                            # Vertical connection - move y down to center bottom of tile and x to center
                            x_pos += self.tile_size // 2
                            y_pos += self.tile_size

                            prev_x += self.tile_size // 2
                        elif prev_room_idx < x:
                            # Diagonal right connection - move x to left side and y to bottom
                            y_pos += self.tile_size
                            x_pos += self.tile_size // 2

                            prev_x += self.tile_size
                        elif prev_room_idx > x:
                            # Diagonal left connection - move x to right side and y to bottom
                            x_pos += self.tile_size // 2
                            y_pos += self.tile_size

                        pygame.draw.line(screen, (255, 255, 255), (prev_x, prev_y),(x_pos, y_pos),
                                            2)
                else:
                    # pygame.draw.rect(screen, (100, 100, 100), (x_pos, y_pos, tile_size, tile_size))
                    pass
        # draw legend
        legend_x = 10
        legend_y = 10
        legend_items = []
        legend_items.append(font.render(self.ROOM_TYPE_SHOP + ": Shop", True, color_map[self.ROOM_TYPE_SHOP]))
        legend_items.append(font.render(self.ROOM_TYPE_REST + ": Rest", True, color_map[self.ROOM_TYPE_REST]))
        legend_items.append(font.render(self.ROOM_TYPE_EVENT + ": Event", True, color_map[self.ROOM_TYPE_EVENT]))
        legend_items.append(font.render(self.ROOM_TYPE_ELITE + ": Elite", True, color_map[self.ROOM_TYPE_ELITE]))
        legend_items.append(font.render(self.ROOM_TYPE_MONSTER + ": Monster", True, color_map[self.ROOM_TYPE_MONSTER]))
        legend_items.append(font.render(self.ROOM_TYPE_CHEST + ": Chest", True, color_map[self.ROOM_TYPE_CHEST]))

        for i, item in enumerate(legend_items):
            screen.blit(item, (legend_x, legend_y + i * 20))

        health_x = 1000
        health_y = 10
        health_text = font.render("Health: " + str(self.player.health) + "/" + str(self.player.start_health), True, "red")
        screen.blit(health_text, (health_x, health_y))

        choice = self.player.controller.get_map_choice(self.player, self, cur_floor, room_idx)
        if choice is not None:
            self.player.controller.reset()
            return choice
        return None

    def handle_event(self, event, screen_size, cur_floor, room_idx):
        avail_floors = self.get_avail_floors(cur_floor, room_idx)
        if event.button == 1:
            pos = pygame.mouse.get_pos()

            self.player.controller.handle_map_event(pos, self.player, self, cur_floor, avail_floors)

    def get_next_room(self, controller):
        while self.player_pos[0] < self.grid_y - 1:
            choice = controller.get_map_choice(self.player, self, self.player_pos[0], self.player_pos[1])
            self.player_pos = (choice.floor, choice.x)
            yield choice
