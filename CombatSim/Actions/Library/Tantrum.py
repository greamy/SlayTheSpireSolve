from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card


class Tantrum(Card):
    def __init__(self, player: Player):
        super().__init__("Tantrum", Card.Type.ATTACK, 1, 3, 3, 1, 0, 0, False, False, player, Player.Stance.WRATH, id=75)
        self.description = "Deal 3 damage 3 times. Enter Wrath. Shuffle this card into your draw pile."
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # Deal 3 damage 3(4) times. Enter {{Wrath}}. Shuffle this card into your draw pile.
        player.deck.draw_pile.append(self)
        player.deck.shuffle()

        return True

    def upgrade(self):
        super().upgrade()
        self.description = "Deal 3 damage 4 times. Enter Wrath. Shuffle this card into your draw pile."
        self.attacks = 4
