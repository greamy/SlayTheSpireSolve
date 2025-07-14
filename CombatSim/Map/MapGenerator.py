import math
import random
import pygame

from CombatSim.Map.ChestRoom import ChestRoom
from CombatSim.Map.EliteRoom import EliteRoom
from CombatSim.Map.EventRoom import EventRoom
from CombatSim.Map.MonsterRoom import MonsterRoom
from CombatSim.Map.RestRoom import RestRoom
from CombatSim.Map.Room import Room
from CombatSim.Map.ShopRoom import ShopRoom


class MapGenerator:
    ROOM_TYPE_CHEST = 'C'
    ROOM_TYPE_ELITE = 'E'
    ROOM_TYPE_EVENT = '?'
    ROOM_TYPE_MONSTER = 'M'
    ROOM_TYPE_REST = 'R'
    ROOM_TYPE_SHOP = 'S'
    ROOM_TYPE_UNSET = 'P' # Node in a path that has not been set to a room type

    def __init__(self, seed=42):
        self.grid_x = 7
        self.grid_y = 15
        self.num_paths = 6
        self.map = None
        self.room_mapping = None

        self.seed = seed
        random.seed(seed)

        self.clear_map()

        # Shops - 0.05 Rest - 0.12 Event - 0.22 Elite - 0.08
        self.shop_chance = 0.05
        self.rest_chance = 0.12
        self.event_chance = 0.22
        self.elite_chance = 0.08

        self.no_dup_room_types = [self.ROOM_TYPE_SHOP, self.ROOM_TYPE_ELITE, self.ROOM_TYPE_REST]

        # rendering attributes:
        self.tile_size = 30
        self.tile_spacing = 15
        self.x_align = 650 - (self.grid_x * self.tile_size + (self.grid_x - 1) * self.tile_spacing)
        self.counter = 0
        self.counter_up = True

    def clear_map(self):
        self.map = [[None for _ in range(self.grid_x)] for _ in range(self.grid_y)]

    def generate_map(self):
        self.clear_map()

        paths = self.generate_paths()

        num_open_nodes, path_map = self.populate_map_with_paths(paths)

        room_counts = {
            self.ROOM_TYPE_SHOP: math.trunc(self.shop_chance * num_open_nodes),
            self.ROOM_TYPE_REST: math.trunc(self.rest_chance * num_open_nodes),
            self.ROOM_TYPE_EVENT: math.trunc(self.event_chance * num_open_nodes),
            self.ROOM_TYPE_ELITE: math.trunc(self.elite_chance * num_open_nodes)
        }
        room_bucket = []

        room_bucket.extend([ShopRoom(0, 0, [], []) for _ in range(room_counts[self.ROOM_TYPE_SHOP])])
        room_bucket.extend([EliteRoom(0, 0, [], []) for _ in range(room_counts[self.ROOM_TYPE_ELITE])])
        room_bucket.extend([EventRoom(0, 0, [], []) for _ in range(room_counts[self.ROOM_TYPE_EVENT])])
        room_bucket.extend([RestRoom(0, 0, [], []) for _ in range(room_counts[self.ROOM_TYPE_REST])])

        # add rest sites to 15th floor, chests to floor 9, and monsters to floor 1.
        pre_typed_rooms = 0
        pre_typed_rooms += self.set_floor_to_type(paths, self.grid_y-1, self.ROOM_TYPE_REST)
        pre_typed_rooms += self.set_floor_to_type(paths, 8, self.ROOM_TYPE_CHEST)
        pre_typed_rooms += self.set_floor_to_type(paths, 0, self.ROOM_TYPE_MONSTER)

        num_open_nodes -= pre_typed_rooms
        room_bucket.extend(MonsterRoom(0, 0, [], []) for _ in range(num_open_nodes - sum(room_counts.values())))
        random.shuffle(room_bucket)

        for p, path in enumerate(paths):
            for floor, room_index in enumerate(path):
                # prev_room = path_map[floor - 1][path[floor - 1]] if floor > 0 else None
                if room_index is not None:
                    prev_rooms = self.room_mapping[floor][room_index]['prev_rooms']
                    if self.map[floor][room_index] is None:
                        # self.Room_links_obj[floor][room_idx] = prev_rooms_x_vals, next_rooms_x_vals
                        unallowed_room_types = self.get_unallowed_room_types(floor, prev_rooms, paths)
                        valid_room = False
                        chosen_room = None
                        for i in range(len(room_bucket)):
                            chosen_room = room_bucket[i]

                            if chosen_room.type not in unallowed_room_types:
                                valid_room = True
                                break
                        if not valid_room:
                            chosen_room = MonsterRoom(floor, room_index, [], [])
                        else:
                            room_bucket.remove(chosen_room)

                        self.map[floor][room_index] = chosen_room
                        chosen_room.prev_rooms = self.room_mapping[floor][room_index]['prev_rooms']
                        chosen_room.next_rooms = self.room_mapping[floor][room_index]['next_rooms']
                        chosen_room.floor = floor
                        chosen_room.x = room_index
                        # self.map[floor][room_index].type = room_type

    def get_unallowed_room_types(self, floor, prev_rooms: list[Room], paths: list[list]):
        # Get a list of room types that are not allowed based on the previous rooms
        unallowed_types = set()

        # Rest, and Elite rooms cannot be below floor 6 (index 5)
        if floor < 5:
            unallowed_types.add(self.ROOM_TYPE_REST)
            unallowed_types.add(self.ROOM_TYPE_ELITE)

        # Rests cannot be on floor 14, because there is a guaranteed rest on floor 15
        if floor == 13:
            unallowed_types.add(self.ROOM_TYPE_REST)

        # no two shops, elites, or rest sites in a row
        for prev_room_idx in prev_rooms:
            if (prev_room_idx is not None and self.map[floor][prev_room_idx] is not None
                    and self.map[floor][prev_room_idx].type in self.no_dup_room_types):
                unallowed_types.add(self.map[floor][prev_room_idx].type)

        # sibling rooms of same parent cannot be the same type
        for prev_room_idx in prev_rooms:
            for next_room in self.room_mapping[floor][prev_room_idx]['next_rooms']:
                if self.map[floor][next_room] is not None:
                    unallowed_types.add(self.map[floor][next_room].type)

        return unallowed_types

    def generate_paths(self):
        paths = [[] for _ in range(self.num_paths)]
        # Generate paths through the map
        for i in range(self.num_paths):
            # Choose random starting node
            start_node_i = random.randint(0, self.grid_x - 1)

            if i == 1:
                # Ensure the second path starts at a different node
                while start_node_i == paths[0][0]:
                    start_node_i = random.randint(0, self.grid_x - 1)

            paths[i].append(start_node_i)

            for j in range(self.grid_y - 1):
                # Choose node nearby to connect to
                low_step = -1
                high_step = 1
                cur_room = paths[i][j]

                # don't allow steps off the edge of the map
                if cur_room == 0:
                    low_step = 0
                elif cur_room == self.grid_x - 1:
                    high_step = 0

                # Don't allow crossed paths
                for k in range(i):
                    if j+1 < len(paths[k]):
                        if paths[k][j] < cur_room and paths[k][j+1] == cur_room:
                            low_step = 0
                        if paths[k][j] > cur_room and paths[k][j+1] == cur_room:
                            high_step = 0

                next_node = cur_room + random.randint(low_step, high_step)
                paths[i].append(next_node)

        # Remove first floor connections to the same node.
        second_floor_connections = []
        for i in range(self.num_paths):
            # check if any starting nodes connect to the same node
            room = paths[i][1]
            if room in second_floor_connections:
                paths[i][0] = None
            else:
                second_floor_connections.append(paths[i][1])

        return paths

    def populate_map_with_paths(self, paths: list[list]):
        # Fill the map with unset rooms on the paths given
        self.room_mapping = [[{"prev_rooms": set(), "next_rooms": set()} for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        local_map = [[None for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        num_open_nodes = 0
        for i in range(self.num_paths):
            for j in range(self.grid_y):
                prev_floor_room_idx = paths[i][j - 1] if j > 0 else None
                next_floor_room_idx = paths[i][j + 1] if j + 1 < self.grid_y else None
                room_idx = paths[i][j]
                if room_idx is not None:
                    if local_map[j][room_idx] is None:
                        local_map[j][room_idx] = "P"
                        num_open_nodes += 1
                    if prev_floor_room_idx is not None:
                        self.room_mapping[j][room_idx]['prev_rooms'].add(prev_floor_room_idx)
                        self.room_mapping[j - 1][prev_floor_room_idx]['next_rooms'].add(room_idx)
                    if next_floor_room_idx is not None:
                        self.room_mapping[j][room_idx]['next_rooms'].add(next_floor_room_idx)
                        self.room_mapping[j + 1][next_floor_room_idx]['prev_rooms'].add(room_idx)

        return num_open_nodes, local_map

    def set_floor_to_type(self, paths: list[list], floor: int, room_type: str):
        num_changed = 0

        for path in paths:
            room_index = path[floor]
            if room_index is not None:
                room = None
                prev_rooms = self.room_mapping[floor][room_index]['prev_rooms']
                next_rooms = self.room_mapping[floor][room_index]['next_rooms']
                if room_type == self.ROOM_TYPE_REST:
                    room = RestRoom(floor, room_index, prev_rooms, next_rooms)
                elif room_type == self.ROOM_TYPE_CHEST:
                    room = ChestRoom(floor, room_index, prev_rooms, next_rooms)
                elif room_type == self.ROOM_TYPE_MONSTER:
                    room = MonsterRoom(floor, room_index, prev_rooms, next_rooms)

                if room is None:
                    raise ValueError("Invalid room type")

                self.map[floor][room_index] = room
                num_changed += 1
        return num_changed

    def calculate_position_from_idx(self, floor_idx, room_idx, screen_size):
        return (self.x_align + room_idx * self.tile_size + room_idx * self.tile_spacing * 2,
                (screen_size[1] - self.tile_size - self.tile_spacing) - (
                            floor_idx * self.tile_size + floor_idx * self.tile_spacing))

    def render(self, screen, screen_size, font):
        # event_room_color = (self.counter,
        #                     (self.counter+32) % 128 if (self.counter+32) % 128 < 64 else 128 - (self.counter+32),
        #                     (self.counter+64) % 128 if (self.counter+64) % 128 < 64 else 128 - (self.counter+64))
                                   # 0,
                            # 0)
                            #        255 - self.counter - 127 if self.counter-127 >  else )
        # print(event_room_color)
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

        for y in range(self.grid_y):
            for x in range(self.grid_x):
                room = self.map[y][x]
                x_pos, y_pos = self.calculate_position_from_idx(y, x, screen_size)
                if room is not None:
                    room.render_map(screen, font, x_pos, y_pos, self.counter, self.tile_size)
                    # pygame.draw.rect(screen, color_map[room.type], (x_pos, y_pos, self.tile_size, self.tile_size))
                    # text = font.render(room.type, True, (0, 0, 0))
                    # screen.blit(text, (x_pos + 5, y_pos + 5))

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
