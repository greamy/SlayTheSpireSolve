from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class FollowUp(Card):
    def __init__(self, player: Player):
        super().__init__("FollowUp", Card.Type.ATTACK, 1, 7, 1, 0, 0, 0, False, False, player, None, id=35)
        self.description = "Deal 7 damage. If the previous card played was an Attack, gain 1 Energy."
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.do_attack)
        self.not_Attack_listener = Listener([Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        self.attack_played = False
        player.add_listener(self.attack_listener)
        player.add_listener(self.not_Attack_listener)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # Deal 7(11) damage. If the previous card played was an Attack, gain 1 {{Energy}}.
        if self.attack_played:
            player.energy += 1

    def do_attack(self, player, enemy, enemies, debug):
        self.attack_played = True

    def do_other(self, player, enemy, enemies, debug):
        self.attack_played = False


    def upgrade(self):
        super().upgrade()
        self.description = "Deal 11 damage. If the previous card played was an Attack, gain 1 Energy."
        self.damage = 11
