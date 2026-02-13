from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class SmilingMask(Relic):
    # The merchant's card removal service now always costs 50 Gold.
    GOLD_AMOUNT = 50
    def __init__(self, player):
        super().__init__("Smiling Mask", "Common", player)
        self.shop_listener = Listener(Listener.Event.ENTER_SHOP, self.on_enter_shop)

    def on_enter_shop(self, player, enemy, enemies, debug):
        # TODO: Set shopkeepers card removal cost to 50 gold
        pass

    def on_pickup(self):
        self.player.add_listener(self.shop_listener)

    def on_drop(self):
        self.player.remove_listener(self.shop_listener)
