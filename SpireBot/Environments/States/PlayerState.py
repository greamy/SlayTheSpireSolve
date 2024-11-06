from CombatSim.Entities.Player import Player
from SpireBot.Environments.States.EntityState import EntityState
import numpy as np

class PlayerState(EntityState):

    def __init__(self, player: Player):
        super().__init__(player)
        self.entity = player

    def get_state(self):
        # [[deck_state], [health, block, max_health, gold], [potions], [relics], [status's]]
        deck_state = self.entity.deck.get_state()

        player_state = np.array([self.entity.health, self.entity.block, self.entity.max_health, self.entity.gold])

        # Status Encoding
        status_ids = np.array([status.id for status in self.entity.status_list])
        status_ids = np.pad(status_ids, (0, max(0, self.MAX_STATUS_ENCODING - len(status_ids))),
                              constant_values=-1)
        player_state = np.append(player_state, status_ids)
        return deck_state, player_state