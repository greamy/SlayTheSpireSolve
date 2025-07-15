from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Vault(Card):
    def __init__(self, player: Player):
        super().__init__("Vault", Card.Type.SKILL, 3, 0, 0, 0, 0, 0, True, False, player, None, id=79)
        self.description = "Take an extra turn after this one. End your turn. Exhaust."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        # Take an extra turn after this one. End your turn. {{Exhaust}}.
        super().play(player, player_list, target_enemy, enemies, debug)
        player.end_turn(enemies, debug)
        player.start_turn(enemies, debug)

        return True