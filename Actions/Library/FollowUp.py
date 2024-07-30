from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class FollowUp(Card):
    def __init__(self):
        super().__init__("FollowUp", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, "", None)
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.do_attack)
        self.not_Attack_listener = Listener([Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        self.attack_played = False
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 7(11) damage. If the previous card played was an Attack, gain 1 {{Energy}}.
    def do_attack(self, player, enemy, enemies, debug):
        self.attack_played = True

    def do_other(self):
        self.attack_played = False


    def upgrade(self):
        super().upgrade()
        self.damage = 11
