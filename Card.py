from Playable import Playable


class Card(Playable):
    def __init__(self, name, energy, damage, attacks, block, draw, discard, exhaust, status):
        super().__init__(damage, attacks, block, status)
        self.name = name
        self.energy = energy
        self.draw = draw
        self.discard = discard
        self.exhaust = exhaust

    def play(self, player, enemy):
        super().play(player, enemy)
        print("Playing " + self.name + "...")
        player.draw_cards(self.draw)
        # TODO: Discard card of player's choice
        # TODO: Do any other effects the card has
        # etc...

    def __str__(self):
        return self.name