from CombatSim.Actions.Card import Card
from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class BlueCandle(Relic):
    # Curse cards can now be played. Playing a Curse will make you lose 1 HP and Exhausts the card.
    def __init__(self, player):
        super().__init__("Blue Candle", "Common", player)
        self.listener = Listener(Listener.Event.CURSE_PLAYED, self.on_curse_play)
        self.add_card_listener = Listener(Listener.Event.CARD_ADDED_TO_DECK, self.on_add_card)

    def on_curse_play(self, player, enemy, enemies, debug):
        lost_health = player.take_damage(1)
        if lost_health:
            player.notify_listeners(Listener.Event.TAKEN_DAMAGE, player, enemies, debug)

    def on_add_card(self, player, enemy, enemies, debug):
        self.set_all_curses()

    def on_pickup(self):
        self.set_all_curses()
        self.player.add_listener(self.listener)
        self.player.add_listener(self.add_card_listener)

    def set_all_curses(self):
        for card in self.player.deck:
            if card.card_type == Card.Type.CURSE:
                card.playable = True
                card.exhaust = True

    def on_drop(self):
        self.player.remove_listener(self.listener)
        self.player.remove_listener(self.add_card_listener)
