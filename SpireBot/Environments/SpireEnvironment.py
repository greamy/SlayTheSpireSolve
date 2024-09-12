import json
import time
from enum import Enum

from spirecomm.communication.action import StartGameAction, ProceedAction, EndTurnAction, CancelAction
from spirecomm.spire.character import PlayerClass
from spirecomm.spire.game import Game

from CombatSim.Entities.Enemy import Enemy
from CombatSim.Entities.Player import Player

from SpireBot.Environments.Environment import Environment
from SpireBot.Environments.States.Map import Map
from SpireBot.InGameCombat import InGameCombat
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


class AllPlayerClasses(Enum):
    IRONCLAD = PlayerClass.IRONCLAD
    THE_SILENT = PlayerClass.THE_SILENT
    DEFECT = PlayerClass.DEFECT
    WATCHER = 4


class SpireEnvironment(Environment):

    def __init__(self, logger: Logger):
        super().__init__()
        self.decoder = json.JSONDecoder()
        self.state: dict = None
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
            return self.bot.combat_choose_next_action(self.state)
        if self.state.end_available:
            self.logger.write("Ending turn...")
            return EndTurnAction()
        if self.state.cancel_available:
            self.logger.write("Cancelling...")
            return CancelAction()
