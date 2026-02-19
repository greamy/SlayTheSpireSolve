from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class InkBottle(Relic):
    # Whenever you play 10 Cards, draw 1 card.
    def __init__(self, player):
        super().__init__("Ink Bottle", "Common", player)
        self.card_listener = Listener(Listener.Event.CARD_PLAYED, self.on_card_played)
        self.card_count = 0

    def on_card_played(self, player, enemy, enemies, debug):
        self.card_count += 1
        if self.card_count == 10:
            player.draw_cards(1, enemies, debug)
            self.card_count = 0

    def on_pickup(self):
        self.player.add_listener(self.card_listener)

    def on_drop(self):
        self.player.remove_listener(self.card_listener)

