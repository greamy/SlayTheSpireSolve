import random
from typing import Generator

from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Enemy import Enemy
from CombatSim.util import createPlayer, addCards, get_default_deck
from GameSim.Map.MonsterRoom import MonsterRoom


class Regimen:

    def __init__(self, max_episodes: int, possible_enemies: list[Enemy], num_enemies: int|list[int], default_deck: list[str],
                 num_additional_cards: int = 0, additional_cards: list[str] = None, allow_repeat_enemies=True, player_max_health=70, player_start_health=70,
                 rest_freq=4, dungeon_path="CombatSim/Entities/Dungeon/", library_path="CombatSim/Actions/Library"):
        self.max_episodes = max_episodes
        self.possible_enemies = possible_enemies
        self.default_deck = default_deck
        self.additional_cards = additional_cards
        self.player_max_health = player_max_health
        self.player_start_health = player_start_health
        self.num_enemies = num_enemies
        self.num_additional_cards = num_additional_cards
        self.allow_repeat_enemies = allow_repeat_enemies
        self.rest_frequency = rest_freq
        self.dungeon_path = dungeon_path
        self.library_path = library_path

    def get_player(self, controller):
        player = createPlayer(controller=controller, health=self.player_start_health, cards=self._get_deck_list(),
                              max_health=self.player_max_health)

        additions = []
        if self.additional_cards is not None and self.num_additional_cards is not None:
            for _ in range(self.num_additional_cards):
                additions.append(random.choice(self.additional_cards))
        cards_in_deck = self.default_deck + additions
        addCards(player, cards_in_deck)
        return player

    def _get_deck_list(self):
        deck = self.default_deck
        if self.additional_cards is not None and self.num_additional_cards is not None:
            for _ in range(self.num_additional_cards):
                deck.append(random.choice(self.additional_cards))
        return deck

    def _get_enemies(self):
        implemented_enemies = Enemy.get_implemented_enemies(self.dungeon_path)
        enemies = []
        allowed_enemies = self.possible_enemies
        enemy_number = self.num_enemies
        if isinstance(self.num_enemies, list):
            enemy_number = random.choice(self.num_enemies)
        for _ in range(enemy_number):
            enemy_choice = random.choice(self.possible_enemies)
            if not self.allow_repeat_enemies:
                allowed_enemies.remove(enemy_choice)
            try:
                enemy_ = getattr(implemented_enemies[enemy_choice], enemy_choice)
                enemies.append(enemy_(ascension=20, act=1))
            except AttributeError:
                enemies = [AcidSlimeSmall(20, 1)]
        return enemies

    # returns a generator that yields rooms for the regimen
    def get_rooms(self, controller) -> Generator[MonsterRoom, None, None]:
        episodes = 0
        player = self.get_player(controller)
        while episodes < self.max_episodes:
            if not player.is_alive():
                player = self.get_player(controller)
            room = MonsterRoom(player,1, 0, [], [], 1, 20)

            room.enemies = self._get_enemies()

            if episodes % self.rest_frequency == 0 and episodes != 0:
                player.health = max(player.health + int(player.max_health * 0.2), player.max_health)

            episodes += 1
            yield room
        print("Regimen completed all episodes. Moving to next regimen if available.")
