import random
from CombatSim.Actions.Listener import Listener
import math

class Entity:

    def __init__(self, health):
        self.health = health
        self.block = 0
        self.damage_dealt_multiplier = 1.0
        self.damage_dealt_modifier = 0
        self.damage_taken_multiplier = 1.0
        self.block_modifier = 0
        self.block_multiplier = 1.0
        self.listeners = []
        self.barricade = False
        self.status_list = []
        self.gold = 0

    def do_turn(self, opponents, debug):
        pass

    def start_turn(self, opponents, debug):
        if not self.barricade:
            self.block = 0
        self.notify_listeners(Listener.Event.START_TURN, opponents, debug)

    def end_turn(self, opponents, debug):
        self.notify_listeners(Listener.Event.END_TURN, opponents, debug)

    def take_damage(self, amount):
        if self.block > 0:
            self.block -= math.floor(amount*self.damage_taken_multiplier)
            if self.block < 0:
                self.health -= abs(self.block)
                self.block = 0
        else:
            self.health -= math.floor(amount*self.damage_taken_multiplier)

        if self.health <= 0:
            self.health = 0

    def gain_block(self, amount, enemies, debug):
        self.block += math.floor((amount + self.block_modifier) * self.block_multiplier)
        self.notify_listeners(Listener.Event.BLOCK_GAINED, enemies, debug)

    def is_alive(self):
        return self.health > 0

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, event_type, enemies, debug):
        if debug:
            pass
            # print("Triggering listeners!")
        for listener in self.listeners:
            if event_type in listener.event_types:
                listener.notify(self, random.choice(enemies), enemies, debug)


