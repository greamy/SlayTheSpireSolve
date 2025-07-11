from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class SpiritShield(Card):
    def __init__(self, player: Player):
        super().__init__("SpiritShield", Card.Type.SKILL, 2, 0, 0, 0, 0, 0, False, False, player, None, id=70)
        self.description = "Gain 3 Block for each card in your hand."
        self.card_block = 3

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Gain 3(4) {{Block}} for each card in your hand.
        self.block = self.card_block * len(player.deck.hand)
        super().play(player, player_list, target_enemy, enemies, debug)

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 4 Block for each card in your hand."
        self.card_block = 4
