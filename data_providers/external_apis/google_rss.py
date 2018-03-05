import base.singleton as sn


import requests
from bs4 import BeautifulSoup
import datetime


class GoogleRss(sn.Singleton):
    # hl sets language to english
    url_template = "https://news.google.com/news/rss/search/section/q/{}?hl=en"

    def get_news_by_keywords(self, keywords, date_from=None, date_to=None):
        url = self.get_url(keywords)
        news_response = requests.get(url)

        soup = BeautifulSoup(news_response.text, "lxml")

        items = soup.find_all("item")
        response = []

        for item in items:
            date = self.get_datetime(item.pubdate.string).date()
            if (date_from is None or date_from <= date) and \
                (date_to is None or date <= date_to):

                new_data = self.get_new_data(item)
                response.append(new_data)

        return response

    def get_datetime(self, datestr):
        return datetime.datetime.strptime(datestr, "%a, %d %b %Y %H:%M:%S %Z")

    def get_new_data(self, new_xml):
        return {
            "title":    new_xml.title.string,
            "link":     new_xml.link.next_sibling,
            "datetime": self.get_datetime(new_xml.pubdate.string)
        }

    def get_url(self, keywords):
        return GoogleRss.url_template.format(" AND ".join(keywords))


if __name__ == "__main__":
    grss = GoogleRss()
    print(grss.get_news(["apple", "microsoft"]))