import pygame

from CombatSim.Entities.Enemy import Enemy
from GameSim.Map.CombatRoom import CombatRoom


class MonsterRoom(CombatRoom):

    def __init__(self, player, floor: int, x: int, prev_rooms: list, next_rooms: list, act, ascension):
        super().__init__(player, "M", floor, x, prev_rooms, next_rooms, act, ascension)
        self.color = (175, 125, 0) # Brown

    def create_enemies(self, act, ascension) -> list[Enemy]:
        if self.player.encounter_pool is None:
            from GameSim.Map.Act1EncounterPool import Act1EncounterPool
            self.player.encounter_pool = Act1EncounterPool()
        return self.player.encounter_pool.get_next_encounter(ascension, act)

    def render_map(self, screen, font, x, y, counter, tile_size, available):
        super().render_map(screen, font, x, y, counter, tile_size, available)
