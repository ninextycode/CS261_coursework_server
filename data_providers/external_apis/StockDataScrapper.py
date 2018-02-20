import datetime
import time
import json
import bs4
import requests
import numpy as np
import pandas as pd

class StockDataScrapper:
    def split_string(self, s, start, end):
        return (s.split(start))[1].split(end)[0].strip()

    def scrape_stocks_data(self, url):
        response = requests.get(url)
        if(response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
            body = table.find('tbody')
            rows = body.findAll('tr')
            arr = []
            for r in rows:
                data = r.findAll('td')
                code = data[0].string
                name = data[1].findChildren()[0].string
                current = data[2].string
                price = data[3].string
                diff = self.split_string(str(data[4]), '">', "<")
                per_diff = data[5].string.strip()
                curr = [code,name,current,price,diff,per_diff]
                arr.append(curr)
            return arr

    '''
    return pandas dataframe of all ftse100 stock's code, name, current, price, diff, per_diff
    '''
    def get_all_stocks_data(self):
        arr1 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1')
        arr2 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=2')
        arr3 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=3')
        arr4 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=4')
        arr5 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=5')
        arr6 = self.scrape_stocks_data('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=6')
        arr = arr1 + arr2 + arr3 + arr4 + arr5 + arr6
        data = np.array(arr)
        dataframe = pd.DataFrame(data=data, columns=['code','name','current','price','diff','per_diff'])
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
                json_obj = json.loads(response.content)
                return json_obj['d'][0][1]
        else:
            print('cannot retrieve data for more than 5 years')

if __name__ == '__main__':
    scrapper = StockDataScrapper()
    print('get_all_stocks_data()')
    print(scrapper.get_all_stocks_data())

    print('get_stocks_historical_data(key,date)')
    date = datetime.datetime(2017,3,20)
    print(scrapper.get_stocks_historical_price("III",date))
    print(scrapper.get_stocks_historical_price("BARC",date))
