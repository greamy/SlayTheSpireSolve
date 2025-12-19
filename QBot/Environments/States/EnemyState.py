from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Status import Status
from QBot.Environments.States.EntityState import EntityState

import numpy as np

class EnemyState(EntityState):
    INTENT_VOCAB_SIZE = 18
    MAX_INTENT_BUF_ENCODING = 3

    def __init__(self, enemy: Enemy):
        super().__init__(enemy)
        self.entity = enemy

    @staticmethod
    def get_len():
        return 3 + EnemyState.INTENT_VOCAB_SIZE + (Status.NUM_STATUSES * EnemyState.MAX_STATUS_ENCODING) + (Status.NUM_STATUSES * EnemyState.MAX_INTENT_BUF_ENCODING) + 2

    def get_state(self):
        # [[health, block, gold], [intent] [status's]]
        state = np.array([self.entity.health, self.entity.block, self.entity.gold])

        # intent
        #[[1-hot encoded kind of intent (ie. Attack, Attack/Block, Attack/Buff..], value (attack value, -1 if na), value 2 (block value), [1-hot encoding kind of buff/debuff]]
        # researching if we should create intent 'embeddings'.. or keep the one-hot encoding
        intent_type_encoding = self.one_hot_encode(np.array([self.entity.intent.intent_type.value], dtype=int), self.INTENT_VOCAB_SIZE, 1)[0]
        encoded_buf = self.one_hot_encode(np.array(self.entity.intent.buff_debuff_ids, dtype=int), Status.NUM_STATUSES, self.MAX_INTENT_BUF_ENCODING)[0]
        state = np.concatenate([state, np.array([self.entity.intent.damage*self.entity.intent.attacks, self.entity.intent.block]), intent_type_encoding.flatten(), encoded_buf.flatten()])

        # Status Encoding
        status_id_list = np.array(self.entity.status_list, dtype=int)
        state = np.append(state, self.one_hot_encode(status_id_list, Status.NUM_STATUSES, self.MAX_STATUS_ENCODING).flatten())

        return state