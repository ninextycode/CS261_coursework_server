import base.singleton as sn
import business_logic.message_routing as routing
import config
import base.log as l
import os
import base.news_page_handler as news_page_handler

import tornado.template as template


logger = l.Logger("HtmlGenerator")


class HtmlGenerator(sn.Singleton):
    def __init__(self):
        self.loader = template.Loader(config.templates_folder)
        self.news_template = self.loader.load("news_template.html")

    @staticmethod
    def static_url(filename):
        return os.path.join(config.static_folder, filename)

    def make_page_for_news(self, news, request):
        logger.log("creating page  for {}".format(request))

        with open(routing.news_page_path, "wb") as new_page:
            page = self.news_template.generate(news=news,
                                               keywords=request["keywords"], static_url=HtmlGenerator.static_url)
            new_page.write(page)
            print("=" * 100)
        news_page_handler.NewsPageHandler.news_page = page

        return page
