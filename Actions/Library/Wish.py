from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Entities.PlatedArmor import PlatedArmor
import random

class Wish(Card):
    def __init__(self, player: Player):
        super().__init__("Wish", Card.Type.SKILL, 3, 0, 0, 0, 0, 0, True, False, player, None)
        self.gold = 25
        self.strength_gain = 3
        self.plated_armor = 6

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Choose one: Gain 6(8) {{Plated Armor}}, 3(4) {{Strength}}, or 25(30) Gold. {{Exhaust}}.
        super().play(player, target_enemy, enemies, debug)
        choice = random.randint(0, 2)
        if choice == 0:
            player.damage_dealt_modifier += self.strength_gain
        elif choice == 1:
            player.gain_gold(self.gold, enemies, debug)
        else:
            PlatedArmor(self.plated_armor, player)

    def upgrade(self):
        super().upgrade()
        self.strength_gain = 4
        self.plated_armor = 8
        self.gold = 30

