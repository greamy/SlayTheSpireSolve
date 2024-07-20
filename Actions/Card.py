from Actions.Playable import Playable
from Entities.Player import Player
from Entities.Enemy import Enemy


class Card(Playable):
    def __init__(self, name, energy, damage, attacks, block, draw, discard, exhaust, status, stance: Player.Stance=None):
        super().__init__(damage, attacks, block, status)
        self.name = name
        self.energy = energy
        self.draw = draw
        self.discard = discard
        self.exhaust = exhaust
        self.stance = stance

    def play(self, player: Player, enemy: Enemy):
        super().play(player, enemy)
        print("Playing " + self.name + "...")
        player.draw_cards(self.draw)

        # TODO: Discard card of player's choice
        # TODO: Do any other effects the card has
        # etc...

        if self.stance is not None:
            player.set_stance(self.stance)

    def __str__(self):
        return self.name
