from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Sanctity(Card):
    def __init__(self, player: Player):
        super().__init__("Sanctity", Card.Type.SKILL, 1, 0, 0, 6, 0, 0, False, False, player, None, id=62)
        self.description = "Gain 6 Block. If the previous card played was a Skill, draw 2 cards."
        self.skill_listener = Listener(Listener.Event.SKILL_PLAYED, self.do_skill)
        self.not_skill_listener = Listener([Listener.Event.ATTACK_PLAYED, Listener.Event.POWER_PLAYED], self.do_other)
        self.skill = False
        self.drawing = 2
        player.add_listener(self.skill_listener)
        player.add_listener(self.not_skill_listener)

    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # TODO: Implement the following:
        if self.skill:
            player.draw_cards(self.drawing, enemies, debug)

        # Gain 6(9) {{Block}}. If the previous card played was a Skill, draw 2 cards.

        return True

    def do_skill(self, player, enemy, enemies, debug):
        self.skill = True

    def do_other(self, player, enemy, enemies, debug):
        self.skill = False


    def upgrade(self):
        super().upgrade()
        self.description = "Gain 9 Block. If the previous card played was a Skill, draw 2 cards."
        self.block = 9
