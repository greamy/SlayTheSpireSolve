
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class CeramicFish(Relic):
    # Whenever you add a card to your deck, gain 9 gold.
    GOLD_AMOUNT = 9
    def __init__(self, player):
        super().__init__("Ceramic Fish", "Common", player)
        self.listener = Listener(Listener.Event.CARD_ADDED_TO_DECK, self.on_card_add)

    def on_card_add(self, player, enemy, enemies, debug):
        player.gold += self.GOLD_AMOUNT

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
