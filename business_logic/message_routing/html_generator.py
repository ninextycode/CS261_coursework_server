import base.singleton as sn
import tornado.template as template
import business_logic.message_routing as routing
import config


class HtmlGenerator(sn.Singleton):
    def __init__(self):
        self.loader = template.Loader(config.templates_folder)
        self.news_template = self.loader.load("news_template.html")

    def get_page_for_news(self, news, request):
        for new in news:
            print(new["summary"])

        with open(routing.news_page_path, "wb") as new_page:
            page = self.news_template.generate(news=news, keywords=request["keywords"])
            new_page.write(page)
