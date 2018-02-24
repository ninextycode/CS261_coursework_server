import base.singleton as sn


class ReadableResponser(sn.Singleton):
    def get_readable_response_to_news(self, data):
        return "Here are the news you asked for {}".format(data)