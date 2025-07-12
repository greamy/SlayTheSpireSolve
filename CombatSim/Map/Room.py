
class Room:
    def __init__(self, type, floor: int, x: int, prev_rooms: list, next_rooms: list):
        self.type = type
        self.prev_rooms = prev_rooms
        self.next_rooms = next_rooms

        self.x = x
        self.floor = floor

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

    def __str__(self):
        return self.type