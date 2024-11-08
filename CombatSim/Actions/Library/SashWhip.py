from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Weak import Weak


class SashWhip(Card):
    def __init__(self, player: Player):
        super().__init__("SashWhip", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, player, None, id=64)
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.do_attack)
        self.other_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        self.attack = False
        self.weak = 1

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        if self.attack:
            weak = Weak(self.weak, target_enemy)
            target_enemy.add_listener(Listener(Listener.Event.START_TURN, weak.decrement))
        self.attack = True
        # Deal 8(10) damage. If the last card played this combat was an Attack, apply 1(2) {{Weak}}.

    def do_attack(self, player, enemy, enemies, debug):
        self.attack = True

    def do_other(self, player, enemy, enemies, debug):
        self.attack = False

    def upgrade(self):
        self.damage = 10
        self.weak = 2