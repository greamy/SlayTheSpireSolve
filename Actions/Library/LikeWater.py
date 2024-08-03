from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class LikeWater(Card):
    def __init__(self, player: Player):
        super().__init__("LikeWater", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.end_turn_block = 5
        self.listener = Listener(Listener.Event.END_TURN, self.do_power)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, if you are in {{Calm}}, gain 5(7) {{Block}}.
        player.add_listener(self.listener)

    def upgrade(self):
        super().upgrade()
        self.end_turn_block = 7

    def do_power(self, player, enemy, enemies, debug):
        if player.stance == player.Stance.CALM:
            player.block += self.end_turn_block
