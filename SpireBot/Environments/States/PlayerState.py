from CombatSim.Entities.Player import Player
from SpireBot.Environments.States.EntityState import EntityState
import numpy as np

class PlayerState(EntityState):

    def __init__(self, player: Player):
        super().__init__(player)
        self.entity = player

        # self.health = player.health
        # self.block = player.block
        # self.relics = None
        # self.potions = None
        # self.deck = None
        # self.gold = None
        # self.max_health = player.max_health

    def get_state(self):
        # [[deck_state], [health, block, max_health, gold], [potions], [relics], [status's]]
        state = self.entity.deck.get_state()

        state = np.append(state, [self.entity.health, self.entity.block, self.entity.max_health, self.entity.gold])

        # Status Encoding
        status_ids = np.array([status.id for status in self.entity.status_list])
        status_ids = np.pad(status_ids, (0, max(0, self.MAX_STATUS_ENCODING - len(status_ids))),
                              constant_values=-1)
        state = np.append(state, status_ids)
        return state