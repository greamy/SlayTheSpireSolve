from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Fasting(Card):
    def __init__(self, player: Player):
        super().__init__("Fasting", Card.Type.POWER, 2, 0, 0, 0, 0, 0, False, False, player, None, id=31)
        self.description = "Gain 3 Strength. Gain 3 Dexterity. Gain 1 less Energy at the start of each turn."
        self.strength = 3
        self.dexterity = 3
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Gain 3(4) {{Strength}}. Gain 3(4) {{Dexterity}}. Gain 1 less {{Energy}} at the start of each turn.
        player.max_energy -= 1
        player.damage_dealt_modifier += self.strength
        player.block_modifier += self.dexterity

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 4 Strength. Gain 4 Dexterity. Gain 1 less Energy at the start of each turn."
        self.strength = 4
        self.dexterity = 4
