from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Rushdown(Card):
    def __init__(self, player: Player):
        super().__init__("Rushdown", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None)
        self.listener = Listener([Listener.Event.ATTACK_PLAYED, Listener.Event.SKILL_PLAYED, Listener.Event.POWER_PLAYED], self.do_card)
        self.drawing_cards = 2
        self.last_stance = player.stance

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        player.add_listener(self.listener)
        self.last_stance = player.stance
        # Whenever you enter {{Wrath}}, draw 2 cards.

    def do_card(self, player, enemy, enemies, debug):
        if player.stance != self.last_stance and player.stance == Player.Stance.WRATH:
            player.draw_cards(self.drawing_cards, enemies, debug)
        self.last_stance = player.stance

    def upgrade(self):
        super().upgrade()
        self.energy = 0
