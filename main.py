from core.server.server import Server


class App:
    def __init__(self):
        self.server = Server()

    def run(self):
        self.server.run()


if __name__ == '__main__':
    App().run()
