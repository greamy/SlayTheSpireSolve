import random

import pygame

from CombatSim.Actions.Listener import Listener
import math

class Entity:

    def __init__(self, health, max_health=None, x=150, y=150, width=100, height=100):
        self.health = health
        self.start_health = max_health if max_health is not None else health
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

    def do_turn(self, allies: list, opponents: list, debug):
        pass

    def start_turn(self, opponents, debug):
        if not self.barricade:
            self.block = 0

    def end_turn(self, opponents, debug):
        pass

    def end_combat(self, opponents, debug):
        self.block_modifier = 0
        self.block_multiplier = 1.0
        self.damage_dealt_modifier = 0
        self.damage_dealt_multiplier = 1.0
        self.damage_taken_multiplier = 1.0

    def take_damage(self, amount) -> bool:
        lost_health = False
        if self.block > 0:
            self.block -= math.floor(amount*self.damage_taken_multiplier)
            if self.block < 0:
                self.health -= abs(self.block)
                lost_health = True
                self.block = 0
        else:
            self.health -= math.floor(amount*self.damage_taken_multiplier)
            lost_health = True

        if self.health <= 0:
            self.health = 0

        return lost_health

    def gain_block(self, amount, enemies, debug):
        self.block += math.floor((amount + self.block_modifier) * self.block_multiplier)

    def is_alive(self):
        return self.health > 0

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def notify_listeners(self, event_type, primary_entity, target_entities, debug):
        for listener in self.listeners:
            if event_type in listener.event_types:
                target_entity = random.choice(target_entities) if target_entities is not None and len(target_entities) > 0 else None
                listener.notify(primary_entity, target_entity, target_entities, debug)

    def render(self, screen, font, text_size=20):
        health_text = font.render("HEALTH:" + str(self.health), True, "green")
        block_text = font.render("BLOCK:" + str(self.block), True, (100, 100, 255))
        screen.blit(health_text, [self.x, self.y - (text_size+5)*2])
        screen.blit(block_text, [self.x, self.y - (text_size+5)])


