from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Card import Card
from CombatSim.Actions.Library.Smite import Smite


class BattleHymn(Card):
    def __init__(self, player: Player):
        super().__init__("BattleHymn", Card.Type.POWER, 1, 0, 0, 0, 0, 0, False, False, player, None, id=2)
        self.description = "At the start of each turn add a Smite into your hand."
        self.listener = Listener(Listener.Event.START_TURN, self.do_power)
        
    def play(self, player: Player, player_list: list[Player], target_enemy: Enemy, enemies: list[Enemy], debug: bool):
        super().play(player, player_list, target_enemy, enemies, debug)
        # (Innate.) At the start of each turn add a {{C|Smite}} into your hand.
        player.add_listener(self.listener)
        return True

    def do_power(self, player, enemy, enemies, debug):
        player.deck.hand.append(Smite(player))

    def upgrade(self):
        super().upgrade()
        self.description = "Innate. " + self.description
        self.innate = True
