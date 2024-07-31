from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Entities.Vulnerable import Vulnerable


class Indignation(Card):
    def __init__(self):
        super().__init__("Indignation", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, "", None)
        self.vulnerable = 3
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        if player.stance == player.Stance.NONE:
            player.stance = player.Stance.WRATH
        elif player.stance == player.Stance.WRATH:
            vuln = Vulnerable(self.vulnerable, target_enemy)
            target_enemy.add_listener(Listener(Listener.Event.START_TURN, vuln.decrement))


        # If you are in {{Wrath}}, apply 3(5) {{Vulnerable}} to ALL enemies, otherwise enter {{Wrath}}.

    def upgrade(self):
        super().upgrade()
        self.vulnerable = 5
