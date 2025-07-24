from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Dazed(Card):
    def __init__(self, player: Player):
        super().__init__("Dazed", Card.Type.STATUS, 0, 0, 0, 0, 0, 0, True, False, player, None, id=16)
        self.description = "Unplayable. Ethereal."
        self.playable = False
        self.ethereal_listener = Listener(Listener.Event.END_TURN, self.do_ethereal)
        player.add_listener(self.ethereal_listener)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Unplayable. {{Ethereal}}
        super().play(player, player_list, target_enemy, enemies, debug)

        return False

    def do_ethereal(self, player, enemy, enemies, debug):
        if self in player.deck.hand:
            player.deck.hand.remove(self)
            player.deck.exhaust_pile.append(self)

    def remove_listeners(self, player: Player):
        player.remove_listener(self.ethereal_listener)
        super().remove_listeners(player)
