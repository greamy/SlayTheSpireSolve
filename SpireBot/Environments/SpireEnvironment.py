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

    # def run(self):
    #     print("READY")
    #     self.get_state()
    #     print("START Watcher 0")
    #     # Click through menus
    #     while True:
    #         time.sleep(1)
    #         self.get_state()
    #         self.process_state(self.state)

    def start_game(self):
        return StartGameAction(AllPlayerClasses.WATCHER)

    def handle_error(self, error):
        self.logger.write(error)