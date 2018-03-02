import base.singleton as sn
import base.log as l
import business_logic.nlp.nlp as nlp
import business_logic.data_tags as tags
import business_logic.message_routing.readable_responser as rr
import business_logic.data_processing.world_data as world_data

logger = l.Logger("MessageRouter")


class MessageRouter(sn.Singleton):

    def set_message_worker(self, message_worker):
        self.message_worker = message_worker

    def __init__(self):
        self.nlp = nlp.NLP.get_instance()
        self.readable_responser = rr.ReadableResponser.get_instance()
        self.world_data = world_data.WorldData.get_instance()

        self.message_worker = None

    def process_alternatives(self, alternatives):
        meaning = self.nlp.get_meaning_from_alternatives(alternatives)
        return self.response_to_formal_request(meaning)

    def process_single(self, message):
        formal_request = self.nlp.get_meaning_from_single(message)
        return self.response_to_formal_request(formal_request)

    def response_to_formal_request(self, formal_request):
        logger.log("received formal request {}".format(formal_request))

        if formal_request["type"] == tags.Type.data_request:
            return self.response_to_data_request(formal_request)
        elif formal_request["type"] == tags.Type.subscription:
            pass  # TODO work on subscriptions

    def response_to_data_request(self, formal_request):
        if formal_request["subtype"] == tags.SubType.news:
            data = self.world_data.get_news(formal_request)
            return self.readable_responser.get_readable_response_for_news(formal_request, data)

        elif formal_request["subtype"] == tags.SubType.social_media:
            data = self.world_data.get_public_opinion(formal_request)
            return self.readable_responser.get_readable_response_for_public_opinion(formal_request, data)

        elif formal_request["subtype"] == tags.SubType.stock:
            pass
            # todo
            # return self.world_data.get_stock_price_data(meaning)


if __name__ == "__main__":
    request0 = {
        "type": tags.Type.data_request,
        "subtype": tags.SubType.social_media,
        "keywords": ["hate"]
    }
    request1 = {
        "type": tags.Type.data_request,
        "subtype": tags.SubType.news,
        "keywords": ["Tesco"]
    }

    router = MessageRouter.get_instance()
    router.response_to_data_request(request0)
    router.response_to_data_request(request1)
