from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Eruption(Card):
    def __init__(self, player: Player):
        super().__init__("Eruption", Card.Type.ATTACK, 2, 9, 1, 0, 0, 0, False, False, player, Player.Stance.WRATH, id=27)
        self.description = "Deal 9 damage. Exit your Stance."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 9 damage. Enter {{Wrath}}.

    def upgrade(self):
        super().upgrade()
        self.energy = 1
