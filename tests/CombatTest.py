import importlib
import unittest
from CombatSim.Actions.Card import Card
from CombatSim.Entities.Player import Player
from CombatSim.Entities.Enemy import Enemy
from CombatSim.Actions.Intent import Intent
from Combat import Combat


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

        self.player = self.createPlayer()
        self.addCards(self.cards)

        self.enemy = self.createEnemy("JawWorm", 20, 1)

    def createPlayer(self):
        return Player(self.health, self.energy, self.gold, self.potions, self.relics, [], "../CombatSim/Actions/Library")

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
        self.player.deck = Player.Deck(cards)

    def test_basic_combat(self):

        combat = Combat(self.player, [self.enemy], True)
        combat.start()

    def test_multiple_enemies(self):
      pass