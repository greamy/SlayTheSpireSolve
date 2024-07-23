from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Meditate(Card):
    def __init__(self):
        super().__init__("Meditate", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, True, "", Player.Stance.CALM)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Put 1(2) card(s) from your discard pile into your hand and {{Retain}} it. Enter {{Calm}}. End your turn.
