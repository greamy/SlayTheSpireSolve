import json
import time
import traceback

from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


class InGameCombat:

    def __init__(self, start_state, environment, player_state, logger: Logger, bot: SpireBot, debug: bool):
        self.player_state = player_state
        self.bot = bot
        self.environment = environment
        self.state = start_state

        self.logger = logger
        self.debug = debug

    def start(self):
        # self.player.begin_combat()
        return self.run()

    def get_total_enemy_health(self):
        return sum([enemy.health for enemy in self.enemies])

    def run(self):
        # First, get state
        # Game loop of player turn:
        #   get possible actions
        #   ask bot to choose action
        #   get new state
        # repeat until no playable cards
        # until 'end turn', then get new state and repeat..

        try:
            # decoder = json.JSONDecoder()
            # state = self.environment.get_state()
            while "play" in self.state['available_commands'] or "end" in self.state["available_commands"]:
                combat_state = self.state["game_state"]['combat_state']

                cards_in_hand = combat_state['hand']
                for index, card in enumerate(cards_in_hand):
                    card['index'] = index
                playable_cards = [card for card in cards_in_hand if card['is_playable']]
                self.logger.write("Playable cards: " + str([card['name'] for card in playable_cards]))

                if len(playable_cards) == 0:
                    print("end")
                    time.sleep(5)
                    continue

                card, enemy = self.bot.combat_choose_next_action(playable_cards, ["enemy1"], None)
                print("play " + str(card['index']) + " 0")
                self.logger.write("play " + card['name'] + " 0")
                time.sleep(1)
                self.state = self.environment.get_state()
        except Exception as e:
            # self.logger.write(str(e))
            # self.logger.err_write(str(e))
            traceback.print_exc(file=self.logger.file)






