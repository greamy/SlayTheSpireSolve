from CombatSim.Actions.Card import Card
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy


class Injury(Card):
    def __init__(self, player: Player):
        super().__init__("Injury", Card.Type.CURSE, 0, 0, 0, 0, 0, 0, False, False, player, None, id=91)
        self.description = "Unplayable."
        self.playable = False

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        return False
