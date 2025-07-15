import importlib
import os
import unittest

from GameSim.Map.CombatRoom import CombatRoom
from CombatSim.Actions.Listener import Listener
from CombatSim.Entities.Player import Player


class EnemyTest(unittest.TestCase):

    def setUp(self):
        self.energy = 3
        self.health = 69
        self.gold = 690
        self.potions = []
        self.relics = []
        self.debug = False

        self.cards = ["Strike" for _ in range(4)]
        self.cards.extend(["Defend" for _ in range(4)])
        self.cards.extend(["Vigilance", "Eruption"])

        self.player = self.createPlayer()
        self.addCards(self.cards)

        self.flag = False

    def addCards(self, name_list: list[str]):
        cards = []
        for name in name_list:
            module = importlib.import_module("CombatSim.Actions.Library." + name)
            class_ = getattr(module, name)
            card = class_(self.player)
            cards.append(card)
        self.player.deck = Player.Deck(cards)

    def createPlayer(self):
        return Player(self.health, self.energy, self.gold, self.potions, self.relics, [], "../CombatSim/Actions/Library")

    def createEnemy(self, name: str, ascension: int, act: int):
        module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
        class_ = getattr(module, name)
        return class_(ascension, act)

    def setFlag(self, enemy, player, player_list, debug):
        self.flag = True

    def test_runAllEnemies(self):
        enemy_file_list = os.listdir(os.path.join(os.curdir, "../CombatSim/Entities/Dungeon"))
        for enemy_file in enemy_file_list:
            if enemy_file.endswith(".py"):
                enemy_file = enemy_file[:-3]
                module = importlib.import_module("CombatSim.Entities.Dungeon." + enemy_file)
                class_ = getattr(module, enemy_file)
                for ascension in range(0, 21):
                    for act in range(1, 4):
                        print("Creating " + enemy_file + " on Ascension " + str(ascension) + " during act " + str(act))
                        enemy = class_(ascension, act)
                        self.player = self.createPlayer()
                        self.addCards(self.cards)

                        start_listener = Listener(Listener.Event.START_TURN, lambda enemy, player, player_list, debug: self.setFlag(enemy, player, player_list, debug))
                        enemy.add_listener(start_listener)

                        enemy.start_turn([self.player], self.debug)
                        self.assertTrue(self.flag)
                        self.flag = False
                        enemy.listeners.remove(start_listener)

                        end_listener = Listener(Listener.Event.END_TURN, lambda enemy, player, player_list, debug: self.setFlag(enemy, player, player_list, debug))
                        enemy.add_listener(end_listener)
                        enemy.do_turn(self.player, self.debug)
                        self.assertTrue(self.flag)
                        self.assertEqual(enemy.num_turns, 1)
                        enemy.listeners.remove(end_listener)

                        combat = CombatRoom(self.player, [enemy], False)
                        num_turn, player_health, is_alive = combat.start()
                        self.assertTrue(num_turn > 0)
                        self.assertTrue(is_alive ^ enemy.is_alive())
                        #print("Player health: " + str(self.player.health))

