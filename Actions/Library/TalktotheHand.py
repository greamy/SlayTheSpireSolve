from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class TalktotheHand(Card):
    def __init__(self):
        super().__init__("TalktotheHand", Card.Type.ATTACK, 1, 5, 1, 0, 0, 0, True, False, "", None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 5(7) damage. Whenever you attack this enemy, gain 2(3) {{Block}}. {{Exhaust}}.
