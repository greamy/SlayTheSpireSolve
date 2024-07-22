from Entities.Player import Player
from Actions.Card import Card
from Actions.Listener import Listener


class Omega(Card):
    def __init__(self):
        super().__init__("Omega", 3, 0, 0, 0, 0, 0, False, "", None)
        self.listener = Listener(Listener.Event.END_TURN, self.listen_action)

    def play(self, player, enemy, debug):
        super().play(player, enemy, debug)
        # TODO: Implement the following:
        # At the end of your turn, deal 50 damage to ALL enemies.
        player.add_listener(self.listener)

    def listen_action(self, player, enemy, debug):
        # TODO: Update to use all enemies
        # for enemy in enemies:
        enemy.take_damage(50)

