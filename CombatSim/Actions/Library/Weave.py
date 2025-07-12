from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Weave(Card):
    def __init__(self, player: Player):
        super().__init__("Weave", Card.Type.ATTACK, 0, 4, 1, 0, 0, 0, False, False, player, None, id=83)
        self.description = "Deal 4 damage. Whenever you Scry, return this from the discard pile to your Hand."
        self.listener = Listener(Listener.Event.SCRY_OCCURRED, self.return_to_hand)
        player.add_listener(self.listener)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Deal 4(6) damage. Whenever you {{Scry}}, return this from the discard pile to your Hand.
        super().play(player, player_list, target_enemy, enemies, debug)

    def return_to_hand(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        if self in player.deck.discard_pile:
            player.deck.discard_pile.remove(self)
            player.deck.hand.append(self)
            player.notify_listeners(Listener.Event.HAND_CHANGED, player, enemies, debug)

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 6 damage. Whenever you Scry, return this from the discard pile to your Hand."
        self.damage = 6
