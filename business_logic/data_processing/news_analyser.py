import data_providers.external_apis.google_rss as google_rss
import business_logic.nlp.data_tags as tags

class NewsAnalyser:
    def __init__(self):
        self.google_rss = google_rss.GoogleRss()

    def get_news(self, json_request):
        news = self.google_rss.get_news(json_request["keywords"],
                                        date_from=json_request.get("date_from", None),
                                        date_to=json_request.get("date_to", None))

        response = {
            "type": tags.Type.data_request,
            "subtype": tags.SubType.news,
            "data": news
        }
        return response
