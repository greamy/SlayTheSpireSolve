import time
import unittest
from GameSim.Map.CombatRoom import CombatRoom
from CombatSim.util import createPlayer, createEnemy, addCards


class CombatTest(unittest.TestCase):

    def setUp(self):
        self.energy = 3
        self.health = 72
        self.gold = 690
        self.potions = []
        self.relics = []
        self.debug = False

        self.cards = ["Strike" for _ in range(4)]
        self.cards.extend(["Defend" for _ in range(4)])
        self.cards.extend(["Vigilance", "Eruption"])
        self.cards.extend(["Devotion" for _ in range(5)])
        self.cards.extend(["SandsofTime" for _ in range(2)])

        self.player = createPlayer()
        addCards(self.player, self.cards)

        self.enemy = createEnemy("SlimeBoss", 20, 1)

    def test_basic_combat(self):
        num_turns = []
        player_healths = []
        num_died = 0
        num_combat = 1
        start = time.time()
        for _ in range(num_combat):
            testing_enemy = createEnemy("SlimeBoss", 20, 1)
            testing_player = createPlayer()
            combat = CombatRoom(testing_player, [testing_enemy], True)
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
