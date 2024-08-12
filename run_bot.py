from SpireBot.Environments.SpireEnvironment import SpireEnvironment
from SpireBot.Logging.Logger import Logger
from SpireBot.SpireBot import SpireBot


def main():
    logger = Logger("C:\\Users\\grant\\PycharmProjects\\SlayTheSpireSolve\\spire_com", ".log")
    env = SpireEnvironment(logger)
    env.run()


if __name__ == '__main__':
    main()
