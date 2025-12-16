import random

from CombatSim.Entities.Dungeon.AcidSlimeSmall import AcidSlimeSmall
from CombatSim.Entities.Enemy import Enemy
from CombatSim.util import createPlayer, addCards, get_default_deck
from GameSim.Map.MonsterRoom import MonsterRoom


class Regimen:

    def __init__(self, num_episodes, possible_enemies: list[Enemy], num_enemies: int|list[int], default_deck: list[str], num_additional_cards: int=0, additional_cards: list[str]=None, player_max_health=70, player_start_health=70, dungeon_path="CombatSim/Entities/Dungeon/", library_path="CombatSim/Actions/Library"):
        self.num_episodes = num_episodes
        self.possible_enemies = possible_enemies
        self.default_deck = default_deck
        self.additional_cards = additional_cards
        self.player_max_health = player_max_health
        self.player_start_health = player_start_health
        self.num_enemies = num_enemies
        self.num_additional_cards = num_additional_cards
        self.dungeon_path = dungeon_path
        self.library_path = library_path

    def get_player(self, controller):
        player = createPlayer(controller=controller)

        additions = []
        if self.additional_cards is not None and self.num_additional_cards is not None:
            for _ in range(self.num_additional_cards):
                additions.append(random.choice(self.additional_cards))
        cards_in_deck = self.default_deck + additions
        addCards(player, cards_in_deck)
        return player

    def get_room(self, player):
        possible_enemies = Enemy.get_implemented_enemies(self.dungeon_path)
        room = MonsterRoom(player,1, 0, [], [], random.randint(1, 2), 20)
        enemies = []
        for _ in range(self.num_enemies):
            enemy_choice = random.choice(self.possible_enemies)
            try:
                enemy_ = getattr(possible_enemies[enemy_choice], enemy_choice)
                enemies.append(enemy_(ascension=20, act=1))
            except AttributeError:
                room.enemies = [AcidSlimeSmall(20, 1)]
        room.enemies = enemies
        return room