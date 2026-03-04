from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Pain(Card):
    def __init__(self, player: Player):
        super().__init__("Pain", Card.Type.CURSE, 0, 0, 0, 0, 0, 0, False, False, player, None, id=90)
        self.description = "Unplayable. While in hand, lose 1 HP when other cards are played."
        self.playable = False

        self.listener = Listener(Listener.Event.CARD_PLAYED, self.on_card_play)
        player.add_listener(self.listener)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Unplayable. At the end of your turn, lose 1 HP for each card in your hand.
        super().play(player, player_list, target_enemy, enemies, debug)

        return False

    def on_card_play(self, player, enemy, enemies, debug):
        if self in player.deck.hand:
            player.health -= 1
            player.notify_listeners(Listener.Event.TAKEN_DAMAGE, player, enemy, debug)

    def add_listeners(self, player: Player):
        player.add_listener(self.listener)


