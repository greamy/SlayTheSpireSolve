from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Crescendo(Card):
    def __init__(self, player: Player):
        super().__init__("Crescendo", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, True, player, Player.Stance.WRATH, id=13)
        self.description = "Enter Wrath. Retain. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # {{Retain}}. Enter {{Wrath}}. {{Exhaust}}.

        return True

    def upgrade(self):
        super().upgrade()
        self.energy = 0
