from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class MentalFortress(Card):
    def __init__(self, player: Player):
        super().__init__("MentalFortress", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None, id=48)
        self.listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED, Listener.Event.ATTACK_PLAYED], self.do_power)
        self.stance_block = 4
        self.last_stance = player.stance

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_listener(self.listener)
        # Whenever you switch {{Stance|Stances}}, gain 4(6) {{Block}}.

    def do_power(self, player, enemy, enemies, debug):
        if self.last_stance != player.stance:
            player.block += self.stance_block
        self.last_stance = player.stance

    def upgrade(self):
        super().upgrade()
        self.stance_block = 6
