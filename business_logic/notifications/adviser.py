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
        popular_companies = []
        for ticker in config.companies.keys():
            n = self.my_data.count_request_with_this_keyword(ticker)
            popular_companies.append((n, ticker))

        popular_companies = sorted(popular_companies, key=lambda x:x[0], reverse=True)
        for i in range(3):
            self.add_subscription_stock(popular_companies[i][1], 0.05)

        for i in range(3, len(popular_companies)):
            self.add_subscription_stock(popular_companies[i][1], 0.1)
