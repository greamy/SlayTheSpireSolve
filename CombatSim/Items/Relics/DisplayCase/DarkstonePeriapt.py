from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic


class DarkstonePeriapt(Relic):
    # Whenever you obtain a Curse, increase your Max HP by 6.
    MAX_HP_GAIN = 6
    def __init__(self, player):
        super().__init__("Darkstone Periapt", "Common", player)
        self.listener = Listener(Listener.Event.CURSE_ADDED, self.on_curse_obtain)

    def on_curse_obtain(self, player, enemy, enemies, debug):
        self.player.add_max_hp(self.MAX_HP_GAIN)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
