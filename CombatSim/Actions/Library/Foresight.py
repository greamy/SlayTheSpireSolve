from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Foresight(Card):
    def __init__(self, player: Player):
        super().__init__("Foresight", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None, id=37)
        self.description = "At the start of your turn, Scry 3"
        self.to_scry = 3
        self.listener = Listener(Listener.Event.START_TURN, self.scry)
        self.scry_amount = 0
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # At the start of your turn, {{Scry}} 3(4).
        player.add_listener(self.listener)

        return True

    def scry(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        self.scry_amount = player.scry(self.to_scry, enemies, debug)
        if self.scry_amount is None:
            return None
        else:
            return True

    def upgrade(self):
        super().upgrade()
        self.description = "At the start of your turn, Scry 4"
        self.to_scry = 4