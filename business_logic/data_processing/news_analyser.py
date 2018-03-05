import base.singleton as sn

import data_providers.data_wrappers.news_provider as news_provider
import business_logic.nlp.nlp as nlp

import multiprocessing.pool as m_pool


class NewsAnalyser(sn.Singleton):
    def __init__(self):
        self.news_provider = news_provider.NewsProvider.get_instance()
        self.nlp = nlp.NLP.get_instance()

    def get_news(self, request_dict):
        date_from = request_dict.get("date_from", None)
        date_to = request_dict.get("date_to", None)
        news = self.news_provider.get_news_by_keywords(request_dict["keywords"],
                                                       date_from=date_from,
                                                       date_to=date_to)
        if len(news) == 0:
            return []

        news = sorted(news, key=lambda x: x["datetime"], reverse=True)
        pool = m_pool.ThreadPool(processes=len(news))

        async_result = pool.map_async(self.nlp.summarise_url, [n["link"] for n in news])
        summaries = async_result.get()

        for i in range(len(news)):
            news[i]["summary"] = summaries[i]

        return news


if __name__ == "__main__":
    news_analyser = NewsAnalyser.get_instance()

    news = news_analyser.get_news({"keywords": ["Tesco"]})
    for n in news:
        print(n)