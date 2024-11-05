from enum import Enum

from CombatSim.Actions.Playable import Playable

class Intent(Playable):
    # class Intent_Type(Enum):
    #     ATTACK = 1
    #     ATTACK_BUFF = 2
    #     ATTACK_DEBUFF = 3
    #     ATTACK_DEFEND = 4
    #     BUFF = 5
    #     DEBUFF = 6
    #     STRONG_DEBUFF = 7
    #     DEBUG = 8
    #     DEFEND = 9
    #     DEFEND_DEBUFF = 10
    #     DEFEND_BUFF = 11
    #     ESCAPE = 12
    #     MAGIC = 13
    #     NONE = 14
    #     SLEEP = 15
    #     STUN = 16
    #     UNKNOWN = 17

    def __init__(self, name, damage, attacks, block, probability, intent_type, buf_debuff_ids=None):
        super().__init__(damage, attacks, block)
        if buf_debuff_ids is None:
            buf_debuff_ids = list()
        self.probability = probability
        self.name = name
        self.intent_type = intent_type
        self.buf_debuff_ids = buf_debuff_ids

    def play(self, enemy, enemy_list, player, player_list, debug):
        if debug:
            print("Playing " + str(self) + "...")
        super().play(enemy, enemy_list, player, player_list, debug)

    def __str__(self):
        return "INTENT: " + self.name + " - " + super().__str__() + " Probability: " + str(self.probability)
