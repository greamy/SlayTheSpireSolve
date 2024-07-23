from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card
from Actions.Library.Smite import Smite


class BattleHymn(Card):
    def __init__(self):
        super().__init__("BattleHymn", Card.Type.POWER, 1, 0, 0, 0, 0, 0, True, "", None)
        self.listener = Listener(Listener.Event.START_TURN, self.do_power)
        
    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        player.deck.hand.append(Smite())

