from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class InnerPeace(Card):
    def __init__(self):
        super().__init__("InnerPeace", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, "", Player.Stance.CALM)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
