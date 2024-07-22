from Entities.Enemy import Enemy
from Entities.Player import Player
from Actions.Card import Card
from Actions.Listener import Listener


class Omega(Card):
    def __init__(self):
        super().__init__("Omega", Card.Type.POWER, 3, 0, 0, 0, 0, 0, True, "", None)
        self.listener = Listener(Listener.Event.END_TURN, self.power)

    def play(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, deal 50 damage to ALL enemies.
        player.add_listener(self.listener)

    def power(self, player, enemy, enemies, debug):
        # TODO: Update to use all enemies
        for enemy in enemies:
            enemy.take_damage(50)

