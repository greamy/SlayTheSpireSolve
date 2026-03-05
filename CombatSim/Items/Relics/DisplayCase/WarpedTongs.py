import random

from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Status.Vulnerable import Vulnerable
from CombatSim.Items.Relics.Relic import Relic

class WarpedTongs(Relic):
    # At the start of your turn, Upgrade a random card in your hand for the rest of combat.

    def __init__(self, player):
        super().__init__("Warped Tongs", "Common", player)

        self.upgraded = []
        self.listener = Listener(Listener.Event.START_TURN, self.start_turn)
        self.end_combat_listener = Listener(Listener.Event.END_COMBAT, self.end_combat_listener)

    def start_turn(self, player, enemy, enemies, debug):
        choice_options = [card for card in player.deck.hand if not card.upgraded]
        if choice_options:
            upgrade_choice = random.choice(choice_options)
            upgrade_choice.upgrade()
            self.upgraded.append(upgrade_choice)

    def end_combat_listener(self, player, enemy, enemies, debug):
        for card in self.upgraded:
            un_upgraded = card.__class__(player)
            player.deck.remove_card(card)
            player.deck.draw_pile.append(un_upgraded)

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.end_combat_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.end_combat_listener)