import base.singleton as sn


class ReadableResponser(sn.Singleton):
    def get_readable_response_for_news(self, request, data):
        print(data)
        return "Placeholder for readable news with data : {}".format(data)

    def get_readable_response_for_public_opinion(self, request, data):
        return "Placeholder for readable social media data with data : {}".format(data)

    def get_readable_response_for_unknown(self):
        return "Sorry, do not understand"