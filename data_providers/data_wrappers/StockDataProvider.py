import sys, os.path
sys.path.append(os.path.abspath('../'))
from external_apis.StockDataScrapper import StockDataScrapper
import requests
import json
import datetime
import time
import numpy as np
import pandas as pd

class StockDataProvider:
    def __init__(self):
        self.scrapper = StockDataScrapper()
    '''
    return pandas dataframe of all ftse100 stock's code, name, current, price, diff, per_diff
    '''
    def get_all_stocks_data(self):
        arr1 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1')
        arr2 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=2')
        arr3 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=3')
        arr4 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=4')
        arr5 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=5')
        arr6 = self.scrapper.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=6')
        arr = arr1 + arr2 + arr3 + arr4 + arr5 + arr6
        data = np.array(arr)
        dataframe = pd.DataFrame(data=data, columns=['code','name','current','price','diff','per_diff','time'])
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

            response = requests.post('http://charts.londonstockexchange.com/WebCharts/services/ChartWService.asmx/GetPrices', json = data)
            if(response.status_code == 200):
                json_obj = response.json()
                return json_obj['d'][0][1]
        else:
            print('cannot retrieve data for more than 5 years')

if __name__ == '__main__':
    dataProvider = StockDataProvider()
    print('get_all_stocks_data()')
    print(dataProvider.get_all_stocks_data())

    print('get_stocks_historical_data(key,date)')
    date = datetime.datetime(2017,3,20)
    print(dataProvider.get_stocks_historical_price("III",date))
    print(dataProvider.get_stocks_historical_price("BARC",date))
