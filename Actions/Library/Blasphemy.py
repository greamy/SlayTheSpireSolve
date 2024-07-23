from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Listener import Listener

class Blasphemy(Card):
    def __init__(self):
        super().__init__("Blasphemy", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, False, "", Player.Stance.DIVINITY)
        self.listener = Listener(Listener.Event.START_TURN, self.do_power)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # (Retain.) Enter Divinity, Die next turn. {{Exhaust}}.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        player.take_damage(999_999)
        player.listeners.remove(self.listener)