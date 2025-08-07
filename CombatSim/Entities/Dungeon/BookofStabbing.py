import random

import spirecomm.spire.character as char

from CombatSim.Actions.Intent import Intent
from CombatSim.Actions.Library.Wound import Wound
from CombatSim.Entities.Enemy import Enemy


# class BookofStabbing(Enemy):
#     MULTISTAB = 0
#     SINGLESTAB = 1
#
#     def __init__(self, ascension: int, act: int):
#
#         intent_set = [self.MultiStab(ascension), self.SingleStab(ascension)]
#
#         if ascension < 8:
#             super().__init__(random.randint(160, 162), intent_set, ascension, minion=False)
#         else:
#             super().__init__(random.randint(168, 172), intent_set, ascension, minion=False)
#
#     def choose_intent(self):
#         pass

