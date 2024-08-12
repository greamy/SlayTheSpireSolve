from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Enemy import Enemy
import random
from CombatSim.Entities.Weak import Weak
from CombatSim.Entities.Player import Player


class RedSlaver(Enemy):
    STAB = 0
    SCRAPE = 1
    ENTANGLE = 2

    def __init__(self, ascension: int, act: int):

        intent_set = [self.Stab(ascension),
                      self.Rake(ascension),
                      self.Entangle(ascension)
                      ]
        if ascension < 7:
            super().__init__(random.randint(46, 50), intent_set, ascension, minion=False)
        else:
            super().__init__(random.randint(48, 52), intent_set, ascension, minion=False)

    def choose_intent(self):
        pass

    def is_valid_intent(self, intent: Intent) -> bool:
        pass

    class Stab(Intent):
        def __init__(self, ascension: int):
            if ascension < 2:
                self.damage = 13
            else:
                self.damage = 14
            super().__init__("Stab", self.damage, 1, 0, 60)

    class Scrape(Intent):
        def __init__(self, ascension: int):

            if ascension < 2:
                self.damage = 8
            else:
                self.damage = 9
            if ascension < 17:
                self.vuln = 1
            else:
                self.vuln = 2
            super().__init__("Scrape", self.damage, 1, 0, 60)