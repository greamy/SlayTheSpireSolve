from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener


class Blasphemy(Card):
    def __init__(self, player):
        super().__init__("Blasphemy", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, True, False, player, Player.Stance.DIVINITY, id=4)
        self.description = "Enter Divinity, Die next turn. Exhaust."
        self.listener = Listener(Listener.Event.START_TURN, self.do_power, 1)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # (Retain.) Enter Divinity, Die next turn. {{Exhaust}}.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        player.take_damage(999_999)

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. " + self.description
        self.retain = True
