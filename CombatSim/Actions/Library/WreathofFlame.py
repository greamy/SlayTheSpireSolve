from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener


class WreathofFlame(Card):
    def __init__(self, player: Player):
        super().__init__("WreathofFlame", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.attack_listener = Listener(Listener.Event.ATTACK_PLAYED, self.temp_strength)
        self.temp_strength_gain = 5

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Your next Attack deals 5(8) additional damage.
        super().play(player, player_list, target_enemy, enemies, debug)
        player.damage_dealt_modifier += self.temp_strength_gain
        player.add_listener(self.attack_listener)

    def temp_strength(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        player.damage_dealt_modifier -= self.temp_strength_gain

    def upgrade(self):
        super().upgrade()
        self.temp_strength_gain = 8


