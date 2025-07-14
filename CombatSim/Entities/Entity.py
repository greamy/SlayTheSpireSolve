import random

import pygame

from CombatSim.Actions.Listener import Listener
import math

class Entity:

    def __init__(self, health, x=150, y=150, width=100, height=100):
        self.health = health
        self.start_health = health
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

        # render attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def do_turn(self, opponents, debug):
        pass

    def start_turn(self, opponents, debug):
        if not self.barricade:
            self.block = 0

    def end_turn(self, opponents, debug):
        pass

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

    def is_alive(self):
        return self.health > 0

    def add_listener(self, listener):
        self.listeners.append(listener)

    def notify_listeners(self, event_type, player, enemies, debug):
        if debug:
            pass
            # print("Triggering listeners!")
        for listener in self.listeners:
            if event_type in listener.event_types:
                listener.notify(player, random.choice(enemies), enemies, debug)

    def render(self, screen, font, text_size=20):
        health_text = font.render("HEALTH:" + str(self.health), True, "green")
        block_text = font.render("BLOCK:" + str(self.block), True, (100, 100, 255))
        screen.blit(health_text, [self.x, self.y - (text_size+5)*2])
        screen.blit(block_text, [self.x, self.y - (text_size+5)])


