from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener

class Perseverance(Card):
    def __init__(self, player: Player):
        super().__init__("Perseverance", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, True, player, None)
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_skill)
        player.add_listener(self.listener)
        self.block_hand_gained = 2

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retain|Retained}}, increase its {{Block}} by 2(3).

    def do_skill(self, player, enemy, enemies, debug):
        self.block += self.block_hand_gained

    def upgrade(self):
        super().upgrade()
        self.block_hand_gained = 3
        self.block += 2
