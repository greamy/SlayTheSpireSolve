from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class MawBank(Relic):
    # Whenever you climb a floor, gain 12 Gold. No longer works when you spend any Gold at the shop.
    GOLD_AMT = 12
    def __init__(self, player):
        super().__init__("Maw Bank", "Common", player)
        self.listener = Listener(Listener.Event.CLIMB_FLOOR, self.on_climb_floor)
        self.shop_listener = Listener(Listener.Event.BUY_FROM_SHOP, self.on_buy_shop)

    def on_climb_floor(self, player, enemy, enemies, debug):
        player.gold += self.GOLD_AMT

    def on_buy_shop(self, player, enemy, enemies, debug):
        player.remove_listener(self.listener)
        player.remove_listener(self.shop_listener)

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.shop_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.shop_listener)
