from external_apis.StockDataScrapper import StockDataScrapper
import pandas as pd
import datetime
import time

def job():
   scrapper = StockDataScrapper()
   df = scrapper.get_all_stocks_data()

   df.to_csv('../data/stocks_csv/'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.csv')

if __name__ == '__main__':
    while True:
        job()
        print("printed")
        time.sleep(10)
