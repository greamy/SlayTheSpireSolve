from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Halt(Card):
    def __init__(self, player: Player):
        super().__init__("Halt", Card.Type.SKILL, 0, 0, 0, 3, 0, 0, False, False, player, None, id=38)
        self.description = "Gain 3(4) Block. Wrath: Gain 9 additional Block."
        self.wrath_block = 9

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)

        if player.stance == player.Stance.WRATH:
            player.block += self.wrath_block

        # Gain 3(4) {{Block}}. {{Wrath}}: Gain 9(14) additional {{Block}}.

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 4 Block. Wrath: Gain 14 additional Block."
        self.block = 4
        self.wrath_block = 14

