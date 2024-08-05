from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Listener import Listener


class Swivel(Card):
    def __init__(self, player: Player):
        super().__init__("Swivel", Card.Type.SKILL, 2, 0, 0, 8, 0, 0, False, False, player, None)
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.refund)
        self.other_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED,
                                        Listener.Event.ENERGY_CHANGED], self.update)
        self.last_energy = player.energy

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Gain 8(11) {{Block}}. The next Attack you play costs 0.
        super().play(player, target_enemy, enemies, debug)
        player.add_listener(self.attack_listener)
        player.add_listener(self.other_listener)
        self.last_energy = player.energy

    def refund(self, player, enemy, enemies, debug):
        player.energy += (self.last_energy - player.energy)
        player.listeners.remove(self.attack_listener)
        player.listeners.remove(self.other_listener)

    def update(self, player, enemy, enemies, debug):
        self.last_energy = player.energy

    def upgrade(self):
        super().upgrade()
        self.block = 11
