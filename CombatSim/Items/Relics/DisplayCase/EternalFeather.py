
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class EternalFeather(Relic):
    # For every 5 cards in your deck, heal 3 HP whenever you enter a Rest Site.
    NUM_CARDS_PER_SET = 5
    HEAL_PER_CARD_SET = 3

    def __init__(self, player):
        super().__init__("Eternal Feather", "Common", player)
        self.listener = Listener(Listener.Event.ENTER_REST, self.on_rest_site)

    def on_rest_site(self, player, enemy, enemies, debug):
        self.player.deck.reshuffle()
        num_cards = len(self.player.deck.draw_pile)
        player.heal((num_cards // self.NUM_CARDS_PER_SET) * self.HEAL_PER_CARD_SET)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
