from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Smite import Smite


class CarveReality(Card):
    def __init__(self, player: Player):
        super().__init__("CarveReality", Card.Type.ATTACK, 1, 6, 1, 0, 0, 0, False, False, player, None, id=8)
        self.description = "Deal 6 damage. Add a Smite into your hand."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        player.deck.hand.append(Smite(player))
        # Deal 6(10) damage. Add a {{C|Smite}} into your hand.

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 6 damage. Add a Smite into your hand."
        self.damage = 10
