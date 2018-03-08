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
