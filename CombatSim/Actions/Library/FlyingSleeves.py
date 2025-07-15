from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class FlyingSleeves(Card):
    def __init__(self, player: Player):
        super().__init__("FlyingSleeves", Card.Type.ATTACK, 1, 4, 2, 0, 0, 0, False, True, player, None, id=34)
        self.description = "Retain. Deal 4 damage twice"
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # {{Retain}}. Deal 4(6) damage twice.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. Deal 6 damage twice."
        self.damage = 6
