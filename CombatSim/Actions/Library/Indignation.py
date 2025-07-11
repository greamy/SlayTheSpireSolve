from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Entities.Status.Vulnerable import Vulnerable


class Indignation(Card):
    def __init__(self, player: Player):
        super().__init__("Indignation", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None, id=39)
        self.description = "If you are in Wrath, apply 3 Vulnerable to ALL enemies. Otherwise, enter Wrath."
        self.vulnerable = 3
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        if player.stance == player.Stance.NONE:
            player.stance = player.Stance.WRATH
        elif player.stance == player.Stance.WRATH:
            vuln = Vulnerable(self.vulnerable, target_enemy)
            target_enemy.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))


        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.

    def upgrade(self):
        super().upgrade()
        self.description = "If you are in Wrath, apply 5 Vulnerable to ALL enemies. Otherwise, enter Wrath."
        self.vulnerable = 5
