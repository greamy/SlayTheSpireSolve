from Entities.Player import Player
from Entities.Enemy import Enemy
from Actions.Card import Card


class InnerPeace(Card):
    def __init__(self):
        super().__init__("InnerPeace", Card.Type.SKILL, 1, 0, 0, 0, 0,
                         0, False, False, "", None)
        self.draw_amount = 3

    def play(self, player: Player, target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, target_enemy, enemies, debug)
        #
        # If you are in {{Calm}}, draw 3(4) cards, otherwise Enter {{Calm}}.
        if player.stance == player.Stance.CALM:
            player.deck.draw_cards(self.draw_amount)
        if player.stance != player.Stance.CALM:
            player.stance = player.Stance.CALM

    def upgrade(self):
        super().upgrade()
        self.draw_amount = 4

