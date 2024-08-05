from Actions.Listener import Listener
from Actions.Playable import Playable
from Entities.Player import Player
from Entities.Enemy import Enemy
from enum import Enum


class Card(Playable):
    def __init__(self, name, card_type, energy, damage, attacks, block, draw, discard, exhaust, retain, player,
                 stance: Player.Stance = None, innate=False, temp_retain=False):
        super().__init__(damage, attacks, block)
        self.name = name
        self.card_type = card_type
        self.energy = energy
        self.draw = draw
        self.discard = discard
        self.exhaust = exhaust
        self.retain = retain
        self.stance = stance
        self.upgraded = False
        self.innate = innate
        self.temp_retain = temp_retain
        self.playable = True

        # Check for Master Reality listener - Upgrade if master reality has been played
        for listener in player.listeners:
            if Listener.Event.CARD_CREATED in listener.event_types:
                self.upgrade()

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        if debug:
            print("Playing " + self.name + "...")
        player.draw_cards(self.draw, enemies, debug)

        # TODO: Discard card of player's choice
        # TODO: Do any other effects the card has
        # etc...
        if self.stance is not None:
            player.set_stance(self.stance)

    def upgrade(self):
        self.upgraded = True

    def is_power(self):
        return self.card_type == self.Type.POWER

    def is_skill(self):
        return self.card_type == self.Type.SKILL

    def is_attack(self):
        return self.card_type == self.Type.ATTACK

    def __str__(self):
        return self.name

    class Type(Enum):
        ATTACK = 0
        SKILL = 1
        POWER = 2
