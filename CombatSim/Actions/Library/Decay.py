from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy


class Decay(Card):
    DAMAGE = 2

    def __init__(self, player: Player):
        super().__init__("Decay", Card.Type.CURSE, 0, 0, 0, 0, 0, 0, False, False, player, None, id=90)
        self.description = "Unplayable. At the end of your turn, take 2 damage."
        self.playable = False
        self.listener = Listener(Listener.Event.END_TURN, self._end_turn_damage)
        player.add_listener(self.listener)

    def _end_turn_damage(self, player, enemy, enemies, debug):
        if self in player.deck.hand:
            player.take_damage(self.DAMAGE)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        return False

    def add_listener(self, player: Player):
        player.add_listener(self.listener)

    def remove_listeners(self, player: Player):
        if self.listener in player.listeners:
            player.remove_listener(self.listener)
