from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener


class Omega(Card):
    def __init__(self, player: Player):
        super().__init__("Omega", Card.Type.POWER, 3, 50, 0, 0, 0, 0, False, False,player, None, id=51)
        self.listener = Listener(Listener.Event.END_TURN, self.do_power)

    def play(self, player: Player, player_list: list[Player], enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, deal 50 damage to ALL enemies.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        for enemy in enemies:
            enemy.take_damage(self.damage)

    def upgrade(self):
        super().upgrade()
        self.damage = 60

