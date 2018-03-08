import base.singleton as sn
import base.log as l
import business_logic.nlp.nlp as nlp
import business_logic.data_tags as tags
import business_logic.message_routing.readable_responser as rr
import business_logic.data_processing.world_data as world_data
import business_logic.data_processing.my_data as my_data
import business_logic.message_routing.html_generator as html_generator
import base.message_worker as mw

logger = l.Logger('MessageRouter')


class MessageRouter(sn.Singleton):

    def set_message_worker(self, message_worker):
        self.message_worker = message_worker

    def __init__(self):
        self.nlp = nlp.NLP.get_instance()
        self.readable_responser: rr.ReadableResponser = rr.ReadableResponser.get_instance()
        self.world_data: world_data.WorldData = world_data.WorldData.get_instance()
        # self.my_data: my_data.MyData = my_data.MyData.get_instance()
        self.html_generator: html_generator.HtmlGenerator = html_generator.HtmlGenerator.get_instance()
        self.message_worker: mw.MessageWorker = None

    def process_alternatives(self, alternatives):
        formal_request = self.nlp.get_meaning_from_alternatives(alternatives)
        self.process_formal_request(formal_request)

    def process_single(self, message):
        formal_request = self.nlp.get_meaning_from_single(message)
        self.process_formal_request(formal_request)

    def process_formal_request(self, request):
        logger.log("request: {}".format(request))
        self.my_data.add_request(request)
        self.send(self.response_to_formal_request(request))

    def send(self, data):
        self.message_worker.send(data)

    def response_to_formal_request(self, formal_request):
        logger.log('received formal request {}'.format(formal_request))

        if formal_request is None:
            return self.unknown_request_response(formal_request)

        if formal_request['type'] == tags.Type.data_request:
            return self.response_to_data_request(formal_request)
        elif formal_request['type'] == tags.Type.subscription:
            pass  # TODO work on subscriptions

        return self.readable_responser.get_readable_response_for_unknown()

    def unknown_request_response(self, formal_request):
        response = {
            'type': tags.OutgoingMessageType.on_unknown_request,
            'data': {
                'body': self.readable_responser.get_readable_response_for_unknown(),
                'mime_type': tags.MimeTypes.text
            },
            'additional_data': {
                'formal_request': formal_request
            }
        }
        return response

    def response_to_data_request(self, formal_request):
        data_subtypes = [
            tags.SubType.news,
            tags.SubType.social_media,
            tags.SubType.stock,
            tags.SubType.industry
        ]
        if formal_request is None or formal_request['subtype'] not in data_subtypes:
            return self.unknown_request_response(formal_request)

        if formal_request['subtype'] == tags.SubType.news:
            unformatted_data = self.world_data.get_news(formal_request)
            html = self.html_generator.make_page_for_news(unformatted_data, formal_request)
            text_response = self.readable_responser.get_readable_response_for_news(unformatted_data, formal_request)
        elif formal_request['subtype'] == tags.SubType.social_media:
            unformatted_data = self.world_data.get_public_opinion(formal_request)
            text_response = \
                self.readable_responser.get_readable_response_for_public_opinion(unformatted_data, formal_request)
        elif formal_request["subtype"] in [tags.SubType.stock, tags.SubType.industry]:
            unformatted_data = self.world_data.get_indicator(formal_request)
            text_response = \
                self.readable_responser.get_readable_response_for_indicator(unformatted_data, formal_request)

        response = {
            'type': tags.OutgoingMessageType.response,
            'data': {
                'body': text_response,
                'mime_type': tags.MimeTypes.text
            },
            'additional_data': {
                'formal_request': formal_request,
                'unformatted_data': unformatted_data
            }
        }

        return response


if __name__ == "__main__":

    tests = [
        #'What is the price of Barclays?',
        #'What do people think about Donald Trump online?',
        #'How is Rolls Royce priced?',
        #'Show me social media trends of Legal and General?',
        #'Find news on Sainsbury's?',
        #'How much does Microsoft cost',
        'What are the news about pork meat in the uk'
    ]

    router: MessageRouter = MessageRouter.get_instance()
    for test in tests:
        result = router.process_single(test)
        print(test, result)
