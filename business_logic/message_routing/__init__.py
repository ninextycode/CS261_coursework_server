import os
import inspect


pages_folder = os.path.join(os.path.join(os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
            os.pardir), os.pardir), "html_pages")

news_page_path = os.path.join(pages_folder, "news.html")
