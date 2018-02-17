import base.Log as l

class MessageWorker:
    instance = None

    @staticmethod
    def get_instance():
        if MessageWorker.instance is None:
            MessageWorker.instance = MessageWorker()
        return MessageWorker.instance

    def __init__(self):
        self.server = None
        self.message_router = None

    def on_message(self, message):
        l.log("Message worker got {} {}".format(type(message), message))

    def send(self, message):
        self.server.send(message)

    def set_server(self, server):
        self.server = server