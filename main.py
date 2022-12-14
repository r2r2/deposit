from core.server.server import server


class App:
    def __init__(self):
        self.server = server

    def run(self):
        self.server.run()


if __name__ == '__main__':
    App().run()
