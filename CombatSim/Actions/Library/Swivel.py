from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener


class Swivel(Card):
    def __init__(self, player: Player):
        super().__init__("Swivel", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, False, player, None, id=73)
        self.description = "Gain 8 Block. The next Attack you play costs 0."
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.refund)
        self.other_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED,
                                        Listener.Event.ENERGY_CHANGED], self.update)
        self.last_energy = player.energy

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Gain 8(11) {{Block}}. The next Attack you play costs 0.
        super().play(player, player_list, target_enemy, enemies, debug)
        player.add_listener(self.attack_listener)
        player.add_listener(self.other_listener)
        self.last_energy = player.energy

        return True

    def refund(self, player, enemy, enemies, debug):
        player.energy += (self.last_energy - player.energy)
        player.listeners.remove(self.attack_listener)
        player.listeners.remove(self.other_listener)

    def update(self, player, enemy, enemies, debug):
        self.last_energy = player.energy

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 11 Block. The next Attack you play costs 0."
        self.block = 11

    def remove_listeners(self, player: Player):
        player.remove_listener(self.attack_listener)
        player.remove_listener(self.other_listener)
        super().remove_listeners(player)
