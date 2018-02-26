import base.log as l
import base.singleton as sn
import business_logic.speech_recognition.text_audio as text_audio

import random
import base64


logger = l.Logger("MessageWorker")


class MessageWorker(sn.Singleton):
    def set_server(self, server):
        self.server = server

    def set_message_router(self, message_router):
        self.message_router = message_router

    def __init__(self):
        self.server = None
        self.message_router = None
        self.text_audio = text_audio.TextAudio.get_instance()

    def on_message(self, message):
        logger.log("from client: {}".format(message))

        message_body = message["body"]
        if message_body["mime_type"] == "text/plain":
            return self.on_text(message_body)
        elif "audio" == message_body["mime_type"].split("/")[0]:
            return self.on_audio(message_body)
        #todo return / throw unknown type error

    def on_audio(self, message_body):
        alternatives = self.text_audio.get_alternatives(message_body)
        return self.message_router.process_alternatives(alternatives)

    def on_text(self, message_body):
        return self.message_router.process_single(message_body["content"])

    def send(self, message):
        self.server.send(message)

