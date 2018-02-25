import base.singleton as sn
import data_providers.external_apis.google_rss as news_api


class NewsProvider(sn.Singleton):
    def __init__(self):
        self.news_apis = [
            news_api.GoogleRss.get_instance(),
            # potentially add more
        ]

    def get_news_by_keywords(self, keywords, date_from, date_to):
        news = []
        news_links = set()

        for api in self.news_apis:
            news_loc = api.get_news_by_keywords(keywords, date_from, date_to)
            for new in news_loc:

                # prevent duplicates
                if new["link"] not in news_links:
                    news_links.add(new["link"])
                    news.append(new)
        return news
