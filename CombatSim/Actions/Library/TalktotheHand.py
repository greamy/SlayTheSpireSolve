from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener

class TalktotheHand(Card):
    def __init__(self, player: Player):
        super().__init__("TalktotheHand", Card.Type.ATTACK, 1, 5, 1, 0, 0, 0, True, False, player, None, id=74)
        self.block_gain = 2
        self.attack_listener = Listener(Listener.Event.TAKEN_DAMAGE, self.gain_block)
        self.enemy = None

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 5(7) damage. Whenever you attack this enemy, gain 2(3) {{Block}}. {{Exhaust}}.
        target_enemy.add_listener(self.attack_listener)
        self.enemy = target_enemy

    def gain_block(self, enemy, player, enemies, debug):
        if enemy == self.enemy:
            player.gain_block(self.block_gain, enemies, debug)

    def upgrade(self):
        super().upgrade()
        self.damage = 7
        self.block_gain = 3

