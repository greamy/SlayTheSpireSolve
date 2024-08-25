import copy
import importlib
import time
import unittest
from CombatSim.Actions.Card import Card
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Intent import Intent
from Combat import Combat


class CombatTest(unittest.TestCase):

    def setUp(self):
        self.energy = 3
        self.health = 60
        self.gold = 690
        self.potions = []
        self.relics = []
        self.debug = False

        self.cards = ["Strike" for _ in range(4)]
        self.cards.extend(["Defend" for _ in range(4)])
        self.cards.extend(["Vigilance", "Eruption"])

        self.player = self.createPlayer()
        self.addCards(self.cards)

        self.enemy = self.createEnemy("GremlinNob", 20, 1)

    def createPlayer(self):
        return Player(self.health, self.energy, self.gold, self.potions, self.relics, [],
                      "../CombatSim/Actions/Library")

    def createEnemy(self, name: str, ascension: int, act: int):
        module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
        class_ = getattr(module, name)
        return class_(ascension, act)

    def addCards(self, name_list: list[str]):
        cards = []
        for name in name_list:
            module = importlib.import_module("CombatSim.Actions.Library." + name)
            class_ = getattr(module, name)
            card = class_(self.player)
            cards.append(card)
        self.player.deck = Player.Deck(cards)

    def test_basic_combat(self):
        num_turns = []
        player_healths = []
        num_died = 0
        num_combat = 1000
        start = time.time()
        for _ in range(num_combat):
            testing_enemy = copy.copy(self.enemy)
            testing_player = copy.copy(self.player)
            combat = Combat(testing_player, [testing_enemy], False)
            num_turn, testing_player.health, is_alive = combat.start()
            num_turns.append(num_turn)
            player_healths.append(testing_player.health)
            num_died += 0 if is_alive else 1
        end = time.time()
        print("The average number of turns for the combat is: " + str(sum(num_turns) / len(num_turns)) +
              "\nThe average remaining health of the player is: " + str(sum(player_healths) / num_combat) +
              "\nThe player died " + str(num_died) + "/" + str(num_combat) + " times.")
        print("Program ran in " + str(end - start) + " seconds.")
        print("The best combat had the player end at " + str(max(player_healths)) + " health with a "
              + str((player_healths.count(max(player_healths)) / num_combat) * 100) + " % chance.")
        print("The worst combat had the player end at " + str(min(player_healths)) + " health with a "
              + str((player_healths.count(min(player_healths)) / num_combat) * 100) + " % chance.\n")

    def test_multiple_enemies(self):
        pass
