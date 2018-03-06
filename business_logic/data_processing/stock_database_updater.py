import base.singleton as sn


import data_providers.data_wrappers.stock_data_provider as stock_data
import data_providers.data_wrappers.sql_database_wrapper as sql_db
import pandas as pd
import time


class StockDatabaseUpdater(sn.Singleton):
    def __init__(self):
        self.provider = stock_data.StockDataProvider.get_instance()
        self.sql_wrapper = sql_db.SqlDatabaseWrapper.get_instance()
        self.currentDf = None
        self.period_sec = 60 * 15

    def update(self):
        dataframe = self.provider.get_all_stocks_data()
        self.sql_wrapper.insert_prices(dataframe)

    def start(self):
        while True:
            self.update()
            time.sleep(self.period_sec / 2)


if __name__ == '__main__':
    StockDatabaseUpdater.get_instance().start()
