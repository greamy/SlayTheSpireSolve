from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class EmptyFist(Card):
    def __init__(self, player: Player):
        super().__init__("EmptyFist", Card.Type.ATTACK, 1, 9, 1, 0, 0, 0, False, False, player, Player.Stance.NONE, id=25)
        self.description = "Deal 14 damage. Exit your Stance."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 9(14) damage. Exit your {{Stance}}.

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 14 damage. Exit your Stance."
        self.damage = 14
