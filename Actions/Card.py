from Actions.Playable import Playable
from Entities.Player import Player
from Entities.Enemy import Enemy
from enum import Enum

class Card(Playable):
    def __init__(self, name, card_type, energy, damage, attacks, block, draw, discard, exhaust, retain, status,
                 stance: Player.Stance = None):
        super().__init__(damage, attacks, block, status)
        self.name = name
        self.type = card_type
        self.energy = energy
        self.draw = draw
        self.discard = discard
        self.exhaust = exhaust
        self.retain = retain
        self.stance = stance

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        if debug:
            print("Playing " + self.name + "...")
        player.draw_cards(self.draw)
        if self.exhaust:
            player.deck.exhaust_pile.append(self)
            player.deck.hand.remove(self)

        # TODO: Discard card of player's choice
        # TODO: Do any other effects the card has
        # etc...

        if self.stance is not None:
            player.set_stance(self.stance)

    def __str__(self):
        return self.name

    class Type(Enum):
        ATTACK = 0
        SKILL = 1
        POWER = 2
