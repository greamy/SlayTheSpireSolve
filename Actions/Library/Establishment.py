from Actions.Listener import Listener
from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class Establishment(Card):
    def __init__(self, player: Player):
        super().__init__("Establishment", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, True, player, None)
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_power)

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # ({{Innate}}.) Whenever a card is {{Retained}}, lower its cost by 1.
        player.add_listener(self.listener)

    def do_power(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            if card.energy > 0:
                card.energy -= 1

    def upgrade(self):
        super().upgrade()
        self.innate = True