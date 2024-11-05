from CombatSim.Entities.Player import Player
from SpireBot.Environments.States.EntityState import EntityState


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
        state = []
        state.append(self.entity.deck.get_state())

        nums = []
        nums.append(self.entity.health)
        nums.append(self.entity.block)
        nums.append(self.entity.max_health)
        nums.append(self.entity.gold)
        state.append(nums)

        # TODO: Potions and relics
        state.append([])
        state.append([])

        # Status Encoding
        state.append([[(1 if self.entity.status_list.id == i else 0) if j < len(self.entity.status_list) else 0 for i in range(30)] for j in range(self.MAX_STATUS_ENCODING)])

        return state