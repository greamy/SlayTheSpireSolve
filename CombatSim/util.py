import importlib

from CombatSim.Entities.Player import Player
from GameSim.Input.RandomPlayerController import RandomPlayerController


def addCards(player, name_list: list[str]):
    cards = []
    for name in name_list:
        module = importlib.import_module("CombatSim.Actions.Library." + name)
        class_ = getattr(module, name)
        card = class_(player)
        cards.append(card)
    player.deck = Player.Deck(cards)


def createPlayer(lib_path='../CombatSim/Actions/Library', controller=RandomPlayerController(),
                 health=70, energy=3, gold=50, potions=None, relics=None, cards=None):
    if relics is None:
        relics = []
    if potions is None:
        potions = []
    if cards is None:
        cards = []
    return Player(health, energy, gold, potions, relics, cards, controller, lib_path)


def createEnemy(name: str, ascension: int, act: int):
    module = importlib.import_module("CombatSim.Entities.Dungeon." + name)
    class_ = getattr(module, name)
    return class_(ascension, act)

def get_default_deck():
    cards = ["Strike" for _ in range(4)]
    cards.extend(["Defend" for _ in range(4)])
    cards.extend(["Vigilance", "Eruption"])
    cards.extend(["Devotion" for _ in range(5)])
    cards.extend(["SandsofTime" for _ in range(2)])
    return cards