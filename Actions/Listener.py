from enum import Enum


class Listener:

    def __init__(self, event_type, on_listen):
        self.event_type = event_type
        self.on_listen = on_listen

    def notify(self, player, enemy, enemies, debug):
        self.on_listen(player, enemy, enemies, debug)

    class Event(Enum):
        START_TURN = 0
        END_TURN = 1
        CARD_RETAINED = 2
        CARD_CREATED = 3
