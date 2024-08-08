from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class SimmeringFury(Card):
    def __init__(self, player: Player):
        super().__init__("SimmeringFury", Card.Type.SKILL, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener(Listener.Event.START_TURN, self.do_card, 1)
        self.drawing_cards = 2

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_listener(self.listener)
        # At the start of your next turn, enter {{Wrath}} and draw 2(3) cards.

    def do_card(self, player: Player, enemy: Enemy, enemies: list[Enemy], debug: bool):
        player.set_stance(Player.Stance.WRATH)
        player.draw_cards(self.drawing_cards, enemies, debug)

    def upgrade(self):
        super().upgrade()
        self.drawing_cards = 3
