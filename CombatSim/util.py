import importlib

from CombatSim.Entities.Player import Player
from CombatSim.Input.RandomPlayerController import RandomPlayerController


def addCards(player, name_list: list[str]):
    cards = []
    for name in name_list:
        module = importlib.import_module("CombatSim.Actions.Library." + name)
        class_ = getattr(module, name)
        card = class_(player)
        cards.append(card)
    player.deck = Player.Deck(cards)


def createPlayer(lib_path='../CombatSim/Actions/Library', health=70, energy=3, gold=50, potions=None, relics=None, cards=None):
    if relics is None:
        relics = []
    if potions is None:
        potions = []
    if cards is None:
        cards = []
    return Player(health, energy, gold, potions, relics, cards, RandomPlayerController(),
                  lib_path)


def createEnemy(name: str, ascension: int, act: int):
    module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
    class_ = getattr(module, name)
    return class_(ascension, act)