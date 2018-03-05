import base.log as l
import base.singleton as sn
import business_logic.speech_recognition.text_audio as text_audio
import business_logic.data_tags as tags


logger = l.Logger("MessageWorker")


class MessageWorker(sn.Singleton):
    def set_server(self, server):
        self.server = server

    def set_message_router(self, message_router):
        self.message_router = message_router

    def __init__(self):
        self.server = None
        self.message_router = None
        self.text_audio: text_audio.TextAudio = text_audio.TextAudio.get_instance()

    def on_message(self, message):
        logger.log("from client: {}".format(message))

        message_body = message["body"]
        if message_body["mime_type"] == "text/plain":
            self.on_text(message_body)
        elif "audio" == message_body["mime_type"].split("/")[0]:
            self.on_audio(message_body)
        else:
            self.send(self.on_unknown_mime_response())

    def on_unknown_mime_response(self):
        return {
            "type": tags.OutgoingMessageType.on_unknown_request,
            "body": {
                "mime_type": tags.MimeTypes.text,
                "body": "Unknown mime type, your post should be either text or audio, "
                        "and it should be explicitly stated in a mime_type field"
            }
        }

    def on_audio(self, message_body):
        alternatives = self.text_audio.get_alternatives(message_body)
        self.message_router.process_alternatives(alternatives)

    def on_text(self, message_body):
        self.message_router.process_single(message_body["content"])

    def send(self, message):
        self.server.send(message)

