from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Listener import Listener

class MasterReality(Card):
    def __init__(self, player: Player):
        super().__init__("MasterReality", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener(Listener.Event.CARD_CREATED, self.do_power)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_listener(self.listener)
        # Whenever a card is created during combat, {{Upgrade}} it.

    def do_power(self, player, enemy, enemies, debug):
        pass

    def upgrade(self):
        self.energy = 0
