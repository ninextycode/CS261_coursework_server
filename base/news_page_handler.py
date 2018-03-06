import tornado.web


class NewsPageHandler(tornado.web.RequestHandler):
    news_page = 'nothing'

    def get(self):
        return self.finish(NewsPageHandler.news_page)