import base.singleton as sn
import base.log as l
import business_logic.nlp.nlp as nlp
import base.data_tags as tags


logger = l.Logger("MessageRouter")


class MessageRouter(sn.Singleton):

    def set_message_worker(self, message_worker):
        self.message_worker = message_worker

    def __init__(self):
        self.nlp = nlp.NLP.get_instance()
        self.message_worker = None
        self.world_data = None

    # todo take alternatives' scores into account
    def process_alternatives(self, alternatives):
        for alt in alternatives:
            try:
                return self.process_single(alt["transcript"])
            except:
                logger.log("failed to undestand one of the alternatives: \"{}\"".format(alt["transcript"]))

    def process_single(self, message):
        meaning = self.nlp.get_meaning(message)
        if meaning["type"] == tags.Type.data_request and \
                meaning["subtype"] == tags.SubType.news:

            return self.world_data.get_news(meaning["keywords"])
