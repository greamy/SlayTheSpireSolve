
class SpireBot:
    def __init__(self):
        self.state = None

    def run(self):
        print("READY")
        self.state = input()
        with open("/spire_com.log", "w") as log_file:
            log_file.write(self.state)
        print("START Watcher 0")
        print(self.state)
