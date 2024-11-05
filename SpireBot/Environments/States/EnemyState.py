from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Status.Status import Status
from SpireBot.Environments.States.EntityState import EntityState


class EnemyState(EntityState):
    INTENT_VOCAB_SIZE = 30

    def __init__(self, enemy: Enemy):
        super().__init__(enemy)
        self.entity = enemy

    def get_state(self):
        # [[health, block, gold], [intent] [status's]]
        state = []

        nums = []
        nums.append(self.entity.health)
        nums.append(self.entity.block)
        nums.append(self.entity.gold)
        state.append(nums)

        # intent
        #[[1-hot encoded kind of intent (ie. Attack, Attack/Block, Attack/Buff..], value (attack value, -1 if na), value 2 (block value), [1-hot encoding kind of buff/debuff]]
        encoded_intent = self.one_hot_encode([self.entity.intent.intent_type], self.INTENT_VOCAB_SIZE, 1)[0]
        encoded_buf = self.one_hot_encode(self.entity.intent.buf_debuff_list, Status.NUM_STATUSES, self.MAX_STATUS_ENCODING)
        state.append([encoded_intent, self.entity.intent.damage*self.entity.intent.attacks, self.entity.intent.block, encoded_buf])

        # Status Encoding
        # state.append([[(1 if self.entity.status_list.id == i else 0) if j < len(self.entity.status_list) else 0 for
        #                i in range(30)] for j in range(self.MAX_STATUS_ENCODING)])
        status_id_list = [status.ID for status in self.entity.status_list]
        state.append(self.one_hot_encode(status_id_list, vocab_size=Status.NUM_STATUSES, max_objects=self.MAX_STATUS_ENCODING))

        return state