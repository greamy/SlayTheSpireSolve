
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class MealTicket(Relic):
    # Whenever you enter a shop room, heal 15 HP.
    HEAL_AMOUNT = 12

    def __init__(self, player):
        super().__init__("Meal Ticket", "Common", player)
        self.shop_listener = Listener(Listener.Event.ENTER_SHOP, self.on_enter_shop)
        self.active = False

    def on_enter_shop(self, player, enemy, enemies, debug):
        player.heal(self.HEAL_AMOUNT)

    def on_pickup(self):
        self.player.add_listener(self.shop_listener)

    def on_drop(self):
        self.player.remove_listener(self.shop_listener)
