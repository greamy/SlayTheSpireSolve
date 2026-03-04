from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Regret(Card):
    def __init__(self, player: Player):
        super().__init__("Regret", Card.Type.CURSE, 0, 0, 0, 0, 0, 0, False, False, player, None, id=90)
        self.description = "Unplayable. At the end of your turn, lose 1 HP for each card in your hand."
        self.playable = False

        self.listener = Listener(Listener.Event.END_TURN, self.on_end_turn)
        player.add_listener(self.listener)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Unplayable. At the end of your turn, lose 1 HP for each card in your hand.
        super().play(player, player_list, target_enemy, enemies, debug)

        return False

    def on_end_turn(self, player, enemy, enemies, debug):
        num_cards = len(player.deck.hand)
        player.health -= num_cards
        player.notify_listeners(Listener.Event.TAKEN_DAMAGE, player, enemy, debug)

    def add_listeners(self, player):
        player.add_listener(self.listener)