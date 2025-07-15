import importlib
import json
import time
from enum import Enum
import random

from spirecomm.communication.action import StartGameAction, ProceedAction, EndTurnAction, CancelAction
from spirecomm.spire.character import PlayerClass
from spirecomm.spire.game import Game
import spirecomm.spire.character as char

from GameSim.Map.Combat import Combat
from CombatSim.Entities.Player import Player

from QBot.Environments.Environment import Environment
from QBot.Logging.Logger import Logger
from QBot.SpireBot import SpireBot


class AllPlayerClasses(Enum):
    IRONCLAD = PlayerClass.IRONCLAD
    THE_SILENT = PlayerClass.THE_SILENT
    DEFECT = PlayerClass.DEFECT
    WATCHER = 4


class SpireEnvironment(Environment):

    def __init__(self, logger: Logger):
        super().__init__()
        self.decoder = json.JSONDecoder()
        self.state: Game = None
        self.bot = SpireBot(logger)
        self.logger = logger

    def start_game(self):
        self.logger.write("Starting Watcher Game")
        return StartGameAction(AllPlayerClasses.WATCHER)

    def handle_error(self, error):
        self.logger.write(error)

    def get_next_action(self, game_state: Game):
        time.sleep(1)
        self.logger.write("Getting next action...")
        self.state = game_state
        if self.state.choice_available:
            self.logger.write("Choice Option Available")
            return self.bot.choose_option(self.state)
        if self.state.proceed_available:
            self.logger.write("Proceeding...")
            return ProceedAction()
        if self.state.play_available:
            self.logger.write("Play card available")
            # TODO: Play potions and cards
            combat = self.create_sim_env()
            playable_cards = [card for card in self.state.hand if card.is_playable]
            return self.bot.combat_choose_next_action(playable_cards, self.state.monsters, combat)
        if self.state.end_available:
            self.logger.write("Ending turn...")
            return EndTurnAction()
        if self.state.cancel_available:
            self.logger.write("Cancelling...")
            return CancelAction()

    def create_cards(self, names: list, player: Player):
        cards = []
        for card in names:
            sanitized_name = card.replace('-', '').replace(' ', '')
            module = importlib.import_module("CombatSim.Actions.Library." + sanitized_name)
            class_ = getattr(module, sanitized_name)
            cards.append(class_(player))
        return cards

    def create_sim_env(self):
        enemies = []
        enemy_intents = []
        for monster in self.state.monsters:
            monster_name = monster.name.replace(" ", "")
            if "(S)" in monster_name:
                monster_name = monster_name.replace("(S)", "Small")
            if "(M)" in monster_name:
                monster_name = monster_name.replace("(M)", "Medium")
            if "(L)" in monster_name:
                monster_name = monster_name.replace("(L)", "Large")
            if "Louse" in monster_name:
                if monster.monster_id == "FuzzyLouseDefensive":
                    monster_name = "GreenLouse"
                else:
                    monster_name = "RedLouse"
            if "Slaver" in monster_name:
                if monster.monster_id == "SlaverBlue":
                    monster_name = "BlueSlaver"
                else:
                    monster_name = "RedSlaver"
            module = importlib.import_module("CombatSim.Entities.Dungeon." + monster_name)
            class_ = getattr(module, monster_name)
            enemy = class_(self.state.ascension_level, self.state.act)
            enemy.health = monster.current_hp
            enemy.block = monster.block

            self.logger.write(monster_name + " intent is " + str(monster.intent))
            possible_intents = [intent for intent in enemy.intent_set if intent.intent_type == monster.intent]
            if len(possible_intents) > 1:
                if monster.intent == char.Intent.ATTACK:
                    enemy.intent = [intent for intent in enemy.intent_set if intent.damage == monster.move_base_damage][0]
                else:
                    enemy.intent = random.choice(enemy.intent)
            else:
                enemy.intent = possible_intents[0]

            enemy_intents.append(enemy.intent)

            self.logger.write("Detected " + monster_name + " intent as " + str(enemy.intent))

            enemies.append(class_(self.state.ascension_level, self.state.act))
        player = Player(self.state.player.current_hp, self.state.player.energy, self.state.gold, self.state.potions, self.state.relics, [])

        player.block = self.state.player.block
        player.energy =self.state.player.energy
        player.health = self.state.player.current_hp
        combat = Combat(player, enemies, debug=False)

        draw_pile = self.create_cards([card.name for card in self.state.draw_pile], player)
        hand = self.create_cards([card.name for card in self.state.hand], player)

        self.logger.write("Starting hand is: " + str(hand))

        discard_pile = self.create_cards([card.name for card in self.state.discard_pile], player)
        exhaust_pile = self.create_cards([card.name for card in self.state.exhaust_pile], player)

        player.deck.hand = hand
        player.deck.draw_pile = draw_pile
        player.deck.discard_pile = discard_pile
        player.deck.exhaust_pile = exhaust_pile

        for i, enemy in enumerate(enemies):
            enemy.health = self.state.monsters[i].current_hp
            enemy.block = self.state.monsters[i].block
            enemy.intent = enemy_intents[i]

        return combat