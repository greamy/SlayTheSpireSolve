import time

from spirecomm.communication.action import ProceedAction
from spirecomm.spire.character import PlayerClass

from SpireBot.Environments.SpireEnvironment import SpireEnvironment
from SpireBot.Environments.SpireEnvironment import AllPlayerClasses
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot
from spirecomm.communication.coordinator import Coordinator


def main():
    logger = Logger("C:\\Users\\Grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")
    # logger = Logger("/Users/grant/PycharmProjects/SlayTheSpireSolve/spire_com", ".log")
    env = SpireEnvironment(logger)
    # env.run()
    try:
        coord = Coordinator()
        # coord.signal_ready()
        print("ready")
        time.sleep(1)
        input()
        print("start WATCHER 0")
        time.sleep(1)
        input()
        print("choose 0")
        time.sleep(1)
        input()
        print("choose 0")
        time.sleep(1)
        input()
        print("proceed")
        time.sleep(1)
        input()
        print("choose 0")
        time.sleep(1)
        logger.write(input())



        coord.register_command_error_callback(env.handle_error)
        coord.register_state_change_callback(env.get_next_action)
        coord.register_out_of_game_callback(env.start_game)
        coord.play_one_game(AllPlayerClasses.WATCHER)
    except Exception as e:
        logger.write(str(e))
    finally:
        logger.close()


if __name__ == '__main__':
    main()
