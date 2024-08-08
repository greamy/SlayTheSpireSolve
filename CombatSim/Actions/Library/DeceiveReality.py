from CombatSim.Actions.Library.Safety import Safety
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class DeceiveReality(Card):
    def __init__(self, player: Player):
        super().__init__("DeceiveReality", Card.Type.SKILL, 1, 0, 0, 4, 0, 0, False, False, player, None)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        player.deck.hand.append(Safety(player))
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.

    def upgrade(self):
        super().upgrade()
        self.block = 7

