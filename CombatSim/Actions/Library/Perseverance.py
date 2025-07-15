from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener

class Perseverance(Card):
    def __init__(self, player: Player):
        super().__init__("Perseverance", Card.Type.SKILL, 1, 0, 0, 5, 0, 0, False, True, player, None, id=53)
        self.description = "Gain 5 Block. Whenever this card is Retained, increase its Block by 2."
        self.listener = Listener(Listener.Event.CARD_RETAINED, self.do_skill)
        player.add_listener(self.listener)
        self.block_hand_gained = 2

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        # {{Retain}}. Gain 5(7) {{Block}}. Whenever this card is {{Retain|Retained}}, increase its {{Block}} by 2(3).

        return True

    def do_skill(self, player, enemy, enemies, debug):
        self.block += self.block_hand_gained

    def upgrade(self):
        super().upgrade()
        self.description = "Gain 7 Block. Whenever this card is Retained, increase its Block by 3."
        self.block_hand_gained = 3
        self.block += 2
