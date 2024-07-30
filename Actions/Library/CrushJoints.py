from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Entities.Vulnerable import Vulnerable


class CrushJoints(Card):
    def __init__(self, player):
        super().__init__("CrushJoints", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, "", None)
        self.vulnerable = 1
        self.skill_played = False
        self.skill_listener = Listener(Listener.Event.SKILL_PLAYED, self.do_skill)
        self.not_skill_listener = Listener([Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        player.add_listener(self.skill_listener)
        player.add_listener(self.not_skill_listener)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.
        if self.skill_played:
            vuln = Vulnerable(self.vulnerable, target_enemy)
            target_enemy.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))
        self.skill_played = False

    def do_skill(self, player, enemy, enemies, debug):
        self.skill_played = True

    def do_other(self, player, enemy, enemies, debug):
        self.skill_played = False

    def upgrade(self):
        super().upgrade()
        self.damage = 10
        self.vulnerable = 2
