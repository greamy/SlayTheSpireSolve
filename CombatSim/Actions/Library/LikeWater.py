from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class LikeWater(Card):
    def __init__(self, player: Player):
        super().__init__("LikeWater", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None, id=45)
        self.description = "At the end of your turn, if you are in Calm, gain 5 Block."
        self.end_turn_block = 5
        self.listener = Listener(Listener.Event.END_TURN, self.do_power)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # At the end of your turn, if you are in {{Calm}}, gain 5(7) {{Block}}.
        player.add_listener(self.listener)

    def upgrade(self):
        super().upgrade()
        self.description = "At the end of your turn, if you are in Calm, gain 7 Block."
        self.end_turn_block = 7

    def do_power(self, player, enemy, enemies, debug):
        if player.stance == player.Stance.CALM:
            player.block += self.end_turn_block
