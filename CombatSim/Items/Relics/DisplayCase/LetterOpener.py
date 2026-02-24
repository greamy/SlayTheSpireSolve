from CombatSim.Actions.Listener import Listener
from CombatSim.Items.Relics.Relic import Relic

class LetterOpener(Relic):
    # Every time you play 3 Skills in a single turn, deal 5 damage to ALL enemies.
    DAMAGE_AMOUNT = 5
    def __init__(self, player):
        super().__init__("Letter Opener", "Common", player)
        self.skill_listener = Listener(Listener.Event.SKILL_PLAYED, self.on_skill_played)
        self.end_turn_listener = Listener(Listener.Event.END_TURN, self.on_end_turn)
        self.skill_count = 0

    def on_skill_played(self, player, enemy, enemies, debug):
        self.skill_count += 1
        if self.skill_count == 3:
            for e in enemies:
                e.take_damage(self.DAMAGE_AMOUNT)
            self.skill_count = 0

    def on_end_turn(self, player, enemy, enemies, debug):
        self.skill_count = 0

    def on_pickup(self):
        self.player.add_listener(self.skill_listener)
        self.player.add_listener(self.end_turn_listener)

    def on_drop(self):
        self.player.remove_listener(self.skill_listener)
        self.player.remove_listener(self.end_turn_listener)

