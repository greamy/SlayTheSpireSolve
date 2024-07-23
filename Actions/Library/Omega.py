from Entities.Enemy import Enemy
from Entities.Player import Player
from Actions.Card import Card
from Actions.Listener import Listener


class Omega(Card):
    def __init__(self):
        super().__init__("Omega", Card.Type.POWER, 3, 50, 0, 0, 0, 0, False, False,"", None)
        self.listener = Listener(Listener.Event.END_TURN, self.do_power)

    def play(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, deal 50 damage to ALL enemies.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        for enemy in enemies:
            enemy.take_damage(self.damage)

    def upgrade(self):
        super().upgrade()
        self.damage = 60

