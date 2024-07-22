from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Omniscience(Card):
    def __init__(self):
        super().__init__("Omniscience", Card.Type.SKILL, 4, 0, 0, 0, 0, 0, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Choose a card in your draw pile. Play the chosen card twice and Exhaust it. Exhaust.
