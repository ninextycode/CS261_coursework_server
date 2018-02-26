import data_providers.external_apis.stock_data_scrapper as scrapper
import base.singleton as sn

import requests
import datetime
import time
import numpy as np
import pandas as pd


class StockDataProvider(sn.Singleton):
    def __init__(self):
        self.scrapper = scrapper.StockDataScrapper.get_instance()
        self.url = "http://www.londonstockexchange.com/exchange/prices-and-markets/" \
                   "stocks/indices/constituents-indices.html?index=UKX&industrySector=&page={}"

    # return pandas dataframe of all ftse100 stock"s code, name, current, price, diff, per_diff
    def get_all_stocks_data(self):
        arr = []
        for i in range(1, 7):
            arr.extend(self.url.join(i))
        data = np.array(arr)
        dataframe = pd.DataFrame(data=data, columns=["code","name","current","price","diff","per_diff","time"])
        return dataframe

    def get_stocks_historical_price(self, stock_code, date):
        today = datetime.date.today()
        if(today.year - date.year < 5 or today.year - date.year == 5 and (today.month < date.month or (today.month == date.month and today.day < date.day))):
            timestamp = time.mktime(date.timetuple())
            data = {"request":{
                    "SampleTime":"1d",
                    "TimeFrame":"5y",
                    "RequestedDataSetType":"ohlc",
                    "ChartPriceType":"price",
                    "Key":stock_code+".LD",
                    "OffSet":"-60",
                    "FromDate":timestamp,
                    "ToDate":timestamp,
                    "UseDelay":"true",
                    "KeyType":"Topic",
                    "KeyType2":"Topic",
                    "Language":"en"
                    }}

            response = requests.post("http://charts.londonstockexchange.com/WebCharts/services/ChartWService.asmx/GetPrices", json = data)
            if(response.status_code == 200):
                json_obj = response.json()
                return json_obj["d"][0][1]
        else:
            print("cannot retrieve data for more than 5 years")


if __name__ == "__main__":
    dataProvider = StockDataProvider()
    print("get_all_stocks_data()")
    print(dataProvider.get_all_stocks_data())

    print("get_stocks_historical_data(key,date)")
    date = datetime.datetime(2017,3,20)
    print(dataProvider.get_stocks_historical_price("III",date))
    print(dataProvider.get_stocks_historical_price("BARC",date))
