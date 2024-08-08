from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Prostrate(Card):
    def __init__(self, player: Player):
        super().__init__("Prostrate", Card.Type.SKILL, 0, 0, 0, 4, 0, 0, False, False, player, None)
        self.mantra = 2
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_mantra(self.mantra)
        # Gain 2(3) {{Mantra}}. Gain 4 {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.mantra = 3
