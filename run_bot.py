from SpireBot.Environments.SpireEnvironment import SpireEnvironment
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot
from spirecomm.communication.coordinator import Coordinator


def main():
    logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")
    env = SpireEnvironment(logger)
    # env.run()

    coord = Coordinator()
    coord.signal_ready()
    coord.register_command_error_callback()
    coord.register_state_change_callback(env.bot.get_next_action)
    coord.register_out_of_game_callback(env.start_game)


if __name__ == '__main__':
    main()
