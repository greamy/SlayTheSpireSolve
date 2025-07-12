from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Worship(Card):
    def __init__(self, player: Player):
        super().__init__("Worship", Card.Type.SKILL, 2, 0, 0, 0, 0, 0, False, False, player, None, id=87)
        self.description = "Gain 5 Mantra."
        self.mantra = 5

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # ({{Retain}}.) Gain 5 {{Mantra}}.
        super().play(player, player_list, target_enemy, enemies, debug)
        player.add_mantra(self.mantra)

    def upgrade(self):
        super().upgrade()
        self.description = "Retain. " + self.description
        self.retain = True

