from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic



class Akabeko(Relic):
    def __init__(self, player):
        super().__init__("Akabeko", "common", player)
        self.player.damage_dealt_modifier +=8
        self.listener = Listener(Listener.Event.ATTACK_PLAYED, self.temp_buff)

    def temp_buff(self, player, enemy, enemies, debug):
        self.player.damage_dealt_multiplier -=8
        self.player.listeners.remove(self.listener)

    def on_pickup(self):
        self.player.add_listener(self.listener)

    def on_drop(self):
        self.player.listeners.remove(self.listener)


