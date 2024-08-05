from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class SandsofTime(Card):
    def __init__(self, player: Player):
        super().__init__("SandsofTime", Card.Type.ATTACK, 4, 20, 1, 0, 0, 0, False, True, player, None)
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_retain)
        player.add_listener(self.listener)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Deal 20(26) damage. Whenever this card is {{Retained}}, lower its cost by 1.

    def do_retain(self, player, enemy, enemies, debug):
        if self.energy > 0 and self in player.deck.hand:
            self.energy -= 1

    def upgrade(self):
        super().upgrade()
        self.damage = 26
