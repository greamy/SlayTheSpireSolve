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
        CARD_PLAYED = 8
        SCRY_OCCURRED = 9
        HAND_CHANGED = 10
        ENERGY_CHANGED = 11
        TAKEN_DAMAGE = 12 # only triggers when HP is lost
        BLOCK_GAINED = 13
        START_COMBAT = 14
        END_COMBAT = 15
        IS_ATTACKED = 16 # Need to make this work for TTLH
        CARD_ADDED_TO_DECK = 17
        CURSE_ADDED = 18
        POWER_ADDED = 19
        ATTACK_ADDED = 20
        SKILL_ADDED = 21
        REST_SITE = 22
        ENTER_SHOP = 23
        ENTER_REST = 24
        BUY_FROM_SHOP = 25
        CLIMB_FLOOR = 26
        ENTER_ELITE = 27
        ENEMY_DIED = 28
        BOSS_START = 29
        SHUFFLE = 30
