import base.Log as l
import random
import base64

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
        message_body = message["body"]
        if message_body["mime_type"] == "text/plain":
            if random.random() < 0.5:
                return
            else:
                raise Exception("Test exception")
        if "audio" == message_body["mime_type"].split("/")[0]:
            self.on_audio(message_body)

    def on_audio(self, message_body):
        ext =  message_body["mime_type"].split("/")[1]
        with open("saved." + ext, "wb") as f:
            print(type(message_body["is_base64"]))
            if message_body["is_base64"]:
                f.write(base64.b64decode(message_body["content"]))
            else:
                f.write(bytes((message_body["content"],)))

    def send(self, message):
        self.server.send(message)

    def set_server(self, server):
        self.server = server