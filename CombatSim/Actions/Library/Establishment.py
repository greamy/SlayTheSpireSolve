from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Establishment(Card):
    def __init__(self, player: Player):
        super().__init__("Establishment", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, True, player, None, id=28)
        self.description = "Whenever a card is Retained, lower its cost by 1."
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_power)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # ({{Innate}}.) Whenever a card is {{Retained}}, lower its cost by 1.
        player.add_listener(self.listener)

        return True

    def do_power(self, player, enemy, enemies, debug):
        for card in player.deck.hand:
            if card.energy > 0:
                card.energy -= 1

    def upgrade(self):
        super().upgrade()
        self.description = "Innate. " + self.description
        self.innate = True