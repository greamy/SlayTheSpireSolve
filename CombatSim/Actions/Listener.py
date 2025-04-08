from enum import Enum


class Listener:

    def __init__(self, event_types, on_listen, num_turns=None):
        if not isinstance(event_types, list):
            event_types = [event_types]
        self.event_types = event_types
        self.on_listen = on_listen
        self.num_turns = num_turns

    def notify(self, player, enemy, enemies, debug):
        if self.num_turns is not None:
            self.num_turns -= 1
            if self.num_turns == 0:
                player.listeners.remove(self)
        self.on_listen(player, enemy, enemies, debug)


    class Event(Enum):
        START_TURN = 0
        END_TURN = 1
        CARD_RETAINED = 2
        CARD_CREATED = 3
        ATTACK_PLAYED = 4
        SKILL_PLAYED = 5
        POWER_PLAYED = 6
        SCRY_OCCURRED = 7
        HAND_CHANGED = 8
        ENERGY_CHANGED = 9
        TAKEN_DAMAGE = 10
        BLOCK_GAINED = 11
        START_COMBAT = 12
        END_COMBAT = 13

