import json
import random
import time

from SpireBot.Logging.Logger import Logger


class SpireBot:
    def __init__(self):
        self.state = None
        self.logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")

    def run(self):
        try:
            decoder = json.JSONDecoder()
            print("READY")
            self.state = input()
            print("START Watcher 0")
            while True:
                time.sleep(1)
                self.state = input()
                self.logger.write(self.state)
                self.state = decoder.decode(self.state)
                self.process_state(self.state)
            self.logger.close()
        except Exception as e:
            self.logger.write(str(e))
            self.logger.err_write(str(e))

    def process_state(self, state):
        try:
            game_ready = state['ready_for_command']
            if not game_ready:
                self.logger.write("Game not ready for commands.")
                return
            commands = state['available_commands']
            if "choose" in commands:
                self.choose_option_random(state)
        except KeyError:
            self.logger.write("State has no available commands.")

    def choose_option_random(self, state):
        try:
            choices = state['game_state']['choice_list']
            self.logger.write(str(choices))
        except KeyError:
            self.logger.write("ERROR: No Choices Available. Might be in combat.")
            return
        choice = random.choice(choices)
        self.logger.write("Chosen " + str(choice) + " from " + str(choices))
        print("CHOOSE " + str(choice))
