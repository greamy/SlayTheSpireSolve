from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Prostrate(Card):
    def __init__(self, player: Player):
        super().__init__("Prostrate", Card.Type.SKILL, 0, 0, 0, 4, 0, 0, False, False, player, None, id=56)
        self.description = "Gain 2 Mantra. Gain 4 Block."
        self.mantra = 2

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_mantra(self.mantra)
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 3 Mantra. Gain 4 Block."
        self.mantra = 3
