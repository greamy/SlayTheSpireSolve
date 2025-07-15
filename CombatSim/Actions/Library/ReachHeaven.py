from CombatSim.Actions.Library.ThroughViolence import ThroughViolence
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class ReachHeaven(Card):
    def __init__(self, player: Player):
        super().__init__("ReachHeaven", Card.Type.ATTACK, 2, 10, 1, 0, 0, 0, False, False, player, None, id=59)
        self.description = "Deal 10 damage. Shuffle a Through Violence into your draw pile."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.deck.draw_pile.append(ThroughViolence(player))
        player.deck.shuffle()
        # Deal 10(15) damage. Shuffle a {{C|Through Violence}} into your draw pile.

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 15 damage. Shuffle a Through Violence into your draw pile."
        self.damage = 15
