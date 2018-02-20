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
                #link = data[1].a['href']
                current = data[2].string
                price = data[3].string
                diff = self.split_string(str(data[4]), '">', "<")
                per_diff = data[5].string.strip()
                curr = [code,name,current,price,diff,per_diff]
                arr.append(curr)
            return arr

    def scrape_stocks_url_key(self, url):
        response = requests.get(url)
        if(response.status_code == 200):
            soup = bs4.BeautifulSoup(response.content, "lxml")
            table = soup.findAll(attrs={"summary" : "Companies and Prices"})[0]
            body = table.find('tbody')
            rows = body.findAll('tr')
            dict = {}
            for r in rows:
                data = r.findAll('td')
                url = data[1].a['href'].replace('/exchange/prices-and-markets/stocks/summary/company-summary/','').replace('.html','')
                dict[data[0].string] = url
            return dict

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

    '''
    return a dictionary of {stock code: stock url key of londonstockexchange.com}
    '''
    def get_all_stocks_url_key(self):
        dict1 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=1')
        dict2 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=2')
        dict3 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=3')
        dict4 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=4')
        dict5 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=5')
        dict6 = self.scrape_stocks_url_key('http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?index=UKX&industrySector=&page=6')
        linkDict = dict(dict1.items() + dict2.items() + dict3.items() + dict4.items() + dict5.items() + dict6.items())
        return linkDict

    '''
    {"request":{"SampleTime":"1d","TimeFrame":"1m","RequestedDataSetType":"ohlc","ChartPriceType":"price","Key":"EZJ.LD","OffSet":-60,"FromDate":1518004800,"ToDate":1518091200,"UseDelay":true,"KeyType":"Topic","KeyType2":"Topic","Language":"en"}}
    '''
    def get_stocks_historical_data(self, urlKey, date):
        data = {"request":{
                "SampleTime":"1d",
                "TimeFrame":"1m",
                "RequestedDataSetType":"ohlc",
                "ChartPriceType":"price",
                "Key":"ABF.LD",
                "OffSet":"-60",
                "FromDate":"1518735600",
                "ToDate":"1518735600",
                "UseDelay":"true",
                "KeyType":"Topic",
                "KeyType2":"Topic",
                "Language":"en"
                }}

        r = requests.post('http://charts.londonstockexchange.com/WebCharts/services/ChartWService.asmx/GetPrices', json = data)
        return r.content


if __name__ == '__main__':
    scrapper = StockDataScrapper()
    print('get_all_stocks_data()')
    print(scrapper.get_all_stocks_data())

    print('get_stocks_historical_data(key,date)')
    print(scrapper.get_stocks_historical_data(1,1))
