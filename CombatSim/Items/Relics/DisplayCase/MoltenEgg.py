from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player
from CombatSim.Items.Relics.Relic import Relic


class MoltenEgg(Relic):
    # Whenever you add a Attack card to your deck, it is Upgraded.
    def __init__(self, player):
        super().__init__("MoltenEgg", "Common", player)
        self.listener = Listener(Listener.Event.CARD_ADDED_TO_DECK, self.on_card_add)
        self.attack_listener = Listener(Listener.Event.ATTACK_ADDED, self.on_attack_add)
        self.cards = []

    def on_card_add(self, player, enemy, enemies, debug):
        self.cards = [card for card in player.deck]

    def on_attack_add(self, player, enemy, enemies, debug):
        for card in self.player.deck:
            if card not in self.cards and card.card_type == Card.Type.ATTACK:
                card.upgrade()
        self.cards = [card for card in player.deck]

    def on_pickup(self):
        self.player.add_listener(self.listener)
        self.player.add_listener(self.attack_listener)

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.attack_listener)

