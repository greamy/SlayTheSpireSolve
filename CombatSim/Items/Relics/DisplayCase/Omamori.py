
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class Omamori(Relic):
    # Negate the next 2 Curses you obtain.
    def __init__(self, player):
        super().__init__("Omamori", "Common", player)
        # self.listener = Listener(Listener.Event.CARD_ADDED_TO_DECK, self.on_card_add)
        self.curse_listener = Listener(Listener.Event.CURSE_ADDED, self.on_curse_add)
        self.num_negates_left = 2
        self.cards = []

    # def on_card_add(self, player, enemy, enemies, debug):
    #     self.cards = [card for card in player.deck]

    def on_curse_add(self, player, enemy, enemies, debug):
        if self.num_negates_left > 0:
            for card in player.deck:
                if card not in self.cards:
                    self.num_negates_left -= 1
                    player.deck.remove_card(card)
            self.cards = [card for card in player.deck]
        else:
            self.player.remove_listener(self.curse_listener)

    def on_pickup(self):
        # self.player.add_listener(self.listener)
        self.player.add_listener(self.curse_listener)

    def on_drop(self):
        # self.player.remove_listener(self.listener)
        self.player.remove_listener(self.curse_listener)
