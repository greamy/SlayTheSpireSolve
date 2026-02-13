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
                if self in player.listeners:
                    player.remove_listener(self)
                else:
                    for e in enemies:
                        if self in player.listeners:
                            e.remove_listener(self)
        self.on_listen(player, enemy, enemies, debug)


    class Event(Enum):
        START_TURN = 0
        END_TURN = 1
        CARD_RETAINED = 2
        CARD_CREATED = 3
        ATTACK_PLAYED = 4
        SKILL_PLAYED = 5
        POWER_PLAYED = 6
        CURSE_PLAYED = 7
        SCRY_OCCURRED = 8
        HAND_CHANGED = 9
        ENERGY_CHANGED = 10
        TAKEN_DAMAGE = 11 # only triggers when HP is lost
        BLOCK_GAINED = 12
        START_COMBAT = 13
        END_COMBAT = 14
        IS_ATTACKED = 15 # Need to make this work for TTLH
        CARD_ADDED_TO_DECK = 16
        CURSE_ADDED = 17
        REST_SITE = 18
        ENTER_SHOP = 19
        BUY_FROM_SHOP = 20
        CLIMB_FLOOR = 21
        ENTER_ELITE = 22
