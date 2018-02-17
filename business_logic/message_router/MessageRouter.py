import business_logic.nlp.NLP as nlp
import base.DataTags as tags


class MessageRouter:
    instance = None

    @staticmethod
    def get_instance():
        if MessageRouter.instance is None:
            MessageRouter.instance = MessageRouter()
        return MessageRouter.instance

    def __init__(self):
        self.nlp = None
        self.message_worker = None
        self.world_data = None

    def initialise(self):
        self.nlp = nlp.NLP.get_instance()

    def process_single(self, message):
        meaning = self.nlp.get_meaning(message)
        if meaning["type"] == tags.Type.data_request and \
                        meaning["subtype"] == tags.SubType.news:

            return self.world_data.get_news(meaning["keywords"])