import base.singleton as sn
import business_logic.data_processing.my_data as my_data
import config
import business_logic.data_tags as tags


class Adviser(sn.Singleton):
    def __init__(self):
        self.my_data: my_data.MyData = my_data.MyData.get_instance()

    def add_subscription_stock(self, ticker, threshold):
        self.my_data.add_subscription({"type":tags.SubType.stock, "ticker": ticker, "threshold": threshold})

    def add_subscription_industry(self, index):
        tickers = config.industry_companies[index]
        print(tickers)
        self.my_data.add_subscription({"type":tags.SubType.industry, "tickers": tickers, "name": config.industries[index][0]})

    def on_new_request(self, request):
        if request is None:
            return
        
        if request["subtype"] == tags.SubType.stock or request["subtype"] == tags.SubType.industry:
            for ticker in request["tickers"]:
                self.on_new_keyword(ticker)
        elif request["subtype"] == tags.SubType.news or request["subtype"] == tags.SubType.social_media:
            for keyword in request["keywords"]:
                self.on_new_keyword(keyword)
        # get tickers of request
        # count
        # if more than 10 set treshold to 0.05

    def on_new_keyword(self, keyword):
        ticker = config.get_ticker(keyword)

        if keyword in config.companies.keys():
            ticker = keyword
            keyword = config.companies["ticker"][0]
        n = self.my_data.count_request_with_this_keyword(ticker)
        if n > 10:
            self.add_subscription_stock(ticker, 0.05)
