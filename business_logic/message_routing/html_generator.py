import base.singleton as sn
import tornado.template as template
import business_logic.message_routing as routing

class HtmlGenerator(sn.Singleton):
    def __init__(self):
        self.loader = template.Loader("./templates")
        self.news_template = self.loader.load("news_template.html")

    def get_page_for_news(self, news):
        for new in news:
            print(new["summary"])

        with open(routing.news_page_path, "wb") as new_page:
            page = self.news_template.generate(news=news)
            new_page.write(page)
