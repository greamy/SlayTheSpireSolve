from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Entities.Status.Vulnerable import Vulnerable


class CrushJoints(Card):
    def __init__(self, player: Player):
        super().__init__("CrushJoints", Card.Type.ATTACK, 1, 8, 1, 0, 0, 0, False, False, player, None, id=14)
        self.description = "Deal 8 damage. If the previous card played was a skill, apply 1(2) Vulnerable."
        self.vulnerable = 1
        self.skill_played = False
        self.skill_listener = Listener(Listener.Event.SKILL_PLAYED, self.do_skill)
        self.not_skill_listener = Listener([Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        player.add_listener(self.skill_listener)
        player.add_listener(self.not_skill_listener)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Deal 8(10) damage. If the previous card played was a skill, apply 1(2) {{Vulnerable}}.
        super().play(player, player_list, target_enemy, enemies, debug)
        if self.skill_played:
            vuln = Vulnerable(self.vulnerable, target_enemy)
            target_enemy.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))
        self.skill_played = False

        return True

    def do_skill(self, player, enemy, enemies, debug):
        self.skill_played = True

    def do_other(self, player, enemy, enemies, debug):
        self.skill_played = False

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 10 damage. If the previous card played was a skill, apply 2 Vulnerable."
        self.damage = 10
        self.vulnerable = 2

    def remove_listeners(self, player: Player):
        player.remove_listener(self.skill_listener)
        player.remove_listener(self.not_skill_listener)
        super().remove_listeners(player)
