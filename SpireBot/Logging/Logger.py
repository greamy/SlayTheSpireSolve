import os


class Logger:

    def __init__(self, path, extension):
        self.file = open(path+extension, 'w')
        self.err = open(path + "_error" + extension, 'w')

    def write(self, data):
        self.file.write(str(data) + "\n")
        if data is str and "error" in data.lower:
            self.err.write(data + "\n")

    def err_write(self, data):
        self.err.write(str(data) + "\n")

    def close(self):
        self.file.close()
        self.err.close()
