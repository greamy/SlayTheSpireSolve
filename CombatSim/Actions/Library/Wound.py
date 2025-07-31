from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Wound(Card):
    def __init__(self, player: Player):
        super().__init__("Wound", Card.Type.STATUS, 0, 0, 0, 0, 0, 0, False, False, player, None, id=89)
        self.description = "Unplayable."
        self.playable = False

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Unplayable. {{Ethereal}}
        super().play(player, player_list, target_enemy, enemies, debug)

        return False
