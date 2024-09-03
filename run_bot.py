from spirecomm.spire.character import PlayerClass

from SpireBot.Environments.SpireEnvironment import SpireEnvironment
from SpireBot.Environments.SpireEnvironment import AllPlayerClasses
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot
from spirecomm.communication.coordinator import Coordinator


def main():
    logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")
    # logger = Logger("/Users/grant/PycharmProjects/SlayTheSpireSolve/spire_com", ".log")
    env = SpireEnvironment(logger)
    # env.run()
    try:
        coord = Coordinator()
        coord.signal_ready()
        coord.register_command_error_callback(env.handle_error)
        coord.register_state_change_callback(env.bot.get_next_action)
        coord.register_out_of_game_callback(env.start_game)
        coord.play_one_game(AllPlayerClasses.WATCHER)
    except Exception as e:
        logger.write(str(e))
    finally:
        logger.close()


if __name__ == '__main__':
    main()
