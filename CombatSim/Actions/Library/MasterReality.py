from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener

class MasterReality(Card):
    def __init__(self, player: Player):
        super().__init__("MasterReality", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener(Listener.Event.CARD_CREATED, self.do_power)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        player.add_listener(self.listener)
        # Whenever a card is created during combat, {{Upgrade}} it.

    def do_power(self, player, enemy, enemies, debug):
        pass

    def upgrade(self):
        self.energy = 0
