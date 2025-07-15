from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class InnerPeace(Card):
    def __init__(self, player: Player):
        super().__init__("InnerPeace", Card.Type.SKILL, 1, 0, 0, 0, 0,
                         0, False, False, player, None, id=40)
        self.description = "If you are in Calm, draw 3 cards. Otherwise, enter Calm."
        self.draw_amount = 3

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        #
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
        if player.stance == player.Stance.CALM:
            player.draw_cards(self.draw_amount, enemies, debug)
        if player.stance != player.Stance.CALM:
            player.stance = player.Stance.CALM

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "If you are in Calm, draw 4 cards. Otherwise, enter Calm."
        self.draw_amount = 4

