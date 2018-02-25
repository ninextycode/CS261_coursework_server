import data_providers.data_wrappers.news_provider as news_p

class WorldData:
    def __init__(self):
        self.news_analyser = None

    def get_news(self, json_request):
        return self.news_analyser.get_news(json_request)