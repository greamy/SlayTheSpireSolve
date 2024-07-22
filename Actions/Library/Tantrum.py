from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Tantrum(Card):
    def __init__(self):
        super().__init__("Tantrum", 1, 3 damage 3, 1, 0, 0, 0, False, "", Player.Stance.WRATH)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 3 damage 3(4) times. Enter {{Wrath}}. Shuffle this card into your draw pile.
