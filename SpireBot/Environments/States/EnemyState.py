from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Status import Status
from SpireBot.Environments.States.EntityState import EntityState

import numpy as np

class EnemyState(EntityState):
    INTENT_VOCAB_SIZE = 30

    def __init__(self, enemy: Enemy):
        super().__init__(enemy)
        self.entity = enemy

    def get_state(self):
        # [[health, block, gold], [intent] [status's]]
        state = np.array([self.entity.health, self.entity.block, self.entity.gold])

        # intent
        #[[1-hot encoded kind of intent (ie. Attack, Attack/Block, Attack/Buff..], value (attack value, -1 if na), value 2 (block value), [1-hot encoding kind of buff/debuff]]
        # researching if we should create intent 'embeddings'.. or keep the one-hot encoding
        intent_type_encoding = self.one_hot_encode(np.array([self.entity.intent.intent_type]), self.INTENT_VOCAB_SIZE, 1)[0]
        encoded_buf = self.one_hot_encode(self.entity.intent.buf_debuff_list, Status.NUM_STATUSES,self.MAX_STATUS_ENCODING)
        state = np.append(state, [intent_type_encoding, self.entity.intent.damage*self.entity.intent.attacks, self.entity.intent.block, encoded_buf])

        # Status Encoding
        status_id_list = np.array([status.ID for status in self.entity.status_list])
        np.append(state, self.one_hot_encode(status_id_list, Status.NUM_STATUSES, self.MAX_STATUS_ENCODING))

        return state