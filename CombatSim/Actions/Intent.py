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
    class IntentRenderColors(Enum):
        ATTACK = (255, 0, 0)
        ATTACK_BUFF = (255, 0, 128)
        ATTACK_DEBUFF = (255, 128, 0)
        ATTACK_DEFEND = (255, 0, 200)
        BUFF = (128, 0, 128)
        DEBUFF = (0, 200, 0)
        STRONG_DEBUFF = (0, 255, 0)
        DEBUG = (50, 50, 50)
        DEFEND = (0, 0, 255)
        DEFEND_DEBUFF = (0, 128, 255)
        DEFEND_BUFF = (0, 128, 128)
        ESCAPE = (255, 255, 0)
        MAGIC = (128, 0, 0)
        NONE = (255, 255, 255)
        SLEEP = (200, 200, 200)
        STUN = (200, 200, 0)
        UNKNOWN = (128, 128, 128)

    def __init__(self, name, damage, attacks, block, probability, intent_type, buff_debuff_ids=None):
        super().__init__(damage, attacks, block)
        if buff_debuff_ids is None:
            buff_debuff_ids = list()
        self.probability = probability
        self.name = name
        self.intent_type = intent_type
        self.buff_debuff_ids = buff_debuff_ids

        # render attributes
        self.color = list(Intent.IntentRenderColors)[intent_type.value - 1].value

    def play(self, enemy, enemy_list, player, player_list, debug):
        if debug:
            print("Playing " + str(self) + "...")
        super().play(enemy, enemy_list, player, player_list, debug)

    def __str__(self):
        return "INTENT: " + self.name + " - " + super().__str__() + " Probability: " + str(self.probability)
