from CombatSim.Actions.Library.Safety import Safety
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class DeceiveReality(Card):
    def __init__(self, player: Player):
        super().__init__("DeceiveReality", Card.Type.SKILL, 1, 0, 0, 4, 0, 0, False, False, player, None, id=18)
        self.description = "Gain 4(7) Block. Add a Safety to your hand."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        player.deck.hand.append(Safety(player))
        # Gain 4(7) {{Block}}. Add a {{C|Safety}} to your hand.

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 7 Block. Add a Safety to your hand."
        self.block = 7

