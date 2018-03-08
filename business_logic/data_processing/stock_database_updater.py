import base.singleton as sn


import data_providers.data_wrappers.stock_data_provider as stock_data
import data_providers.data_wrappers.sql_database_wrapper as sql_db
import data_providers.data_wrappers.mysql_scripts.random_data as random_data
import pandas as pd
import time
import threading


class StockDatabaseUpdater(sn.Singleton):
    def __init__(self):
        self.provider = stock_data.StockDataProvider.get_instance()
        self.sql_wrapper = sql_db.SqlDatabaseWrapper.get_instance()
        self.currentDf = None
        self.period_sec = 60 * 1
        self.random_data_provider = random_data.RandomData.get_instance()

    def update(self):
        # dataframe = self.provider.get_all_stocks_data()
        # self.sql_wrapper.insert_prices(dataframe)
        self.random_data_provider.new_random_prices()

    def start(self):
        def checker():
            while True:
                self.update()
                time.sleep(self.period_sec / 2)

        th = threading.Thread(target=checker)
        th.daemon = True
        th.start()


if __name__ == '__main__':
    StockDatabaseUpdater.get_instance().start()
