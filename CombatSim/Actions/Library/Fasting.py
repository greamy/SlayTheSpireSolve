from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Fasting(Card):
    def __init__(self, player: Player):
        super().__init__("Fasting", Card.Type.POWER, 2, 0, 0, 0, 0, 0, False, False, player, None)
        self.strength = 3
        self.dexterity = 3
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Strength}}. Gain 3(4) {{Dexterity}}. Gain 1 less {{Energy}} at the start of each turn.
        player.damage_dealt_modifier += self.strength
        player.block_modifier += self.dexterity

    def upgrade(self):
        super().upgrade()
        self.strength = 4
        self.dexterity = 4
