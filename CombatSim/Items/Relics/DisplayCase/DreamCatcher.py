
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class DreamCatcher(Relic):
    # Whenever you rest, you may add a card to your deck.
    GOLD_AMOUNT = 9
    def __init__(self, player):
        super().__init__("Dream Catcher", "Common", player)
        self.listener = Listener(Listener.Event.REST_SITE, self.on_rest_site)

    def on_rest_site(self, player, enemy, enemies, debug):
        # TODO: Implement a real card choice!
        player.add_card("TalktotheHand")

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
