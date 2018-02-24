import base.singleton as sn
import base.log as l
import business_logic.nlp.nlp as nlp
import business_logic.nlp.data_tags as tags
import business_logic.message_routing.readable_responser as rr

logger = l.Logger("MessageRouter")


class MessageRouter(sn.Singleton):

    def set_message_worker(self, message_worker):
        self.message_worker = message_worker

    def __init__(self):
        self.nlp = nlp.NLP.get_instance()
        self.readable_responser = rr.ReadableResponser.get_instance()
        self.message_worker = None
        self.world_data = None

    def process_alternatives(self, alternatives):
        meaning = self.nlp.get_meaning_from_alternatives(alternatives)
        return self.response_to_command(meaning)

    def process_single(self, message):
        meaning = self.nlp.get_meaning_from_single(message)
        return self.response_to_command(meaning)

    def response_to_command(self, meaning):
        if meaning["type"] == tags.Type.data_request:
            return self.response_to_data_request(meaning)
        elif meaning["type"] == tags.Type.subscription:
            pass  # TODO work on subscriptions


    def response_to_data_request(self, meaning):
        if meaning["subtype"] == tags.SubType.news:
            data = self.world_data.get_news(meaning["keywords"])
            return self.readable_responser.get_readable_response_to_news(data)
        elif meaning["subtype"] == tags.SubType.social_media:
            return self.world_data.get_social_media_data(meaning["keywords"])
        elif meaning["subtype"] == tags.SubType.stock:
            return self.world_data.get_stock_price_data(meaning["keywords"])