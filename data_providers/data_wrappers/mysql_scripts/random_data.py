import sys
sys.path.extend(['/server',
                 '/server/data_providers/data_wrappers/mysql_scripts'])



import data_providers.data_wrappers.stock_data_provider as stock_data_provider
import data_providers.data_wrappers.sql_database_wrapper as sql_database_wrapper
import base.singleton as sn
import datetime

import numpy as np
import pandas as pd
import decimal

import random
# 7:50 a.m. with an opening auction and ends at 4:35 p.m


class RandomData(sn.Singleton):
    def __init__(self):
        self.start_time = datetime.time(0, 00)
        self.end_time = datetime.time(23, 45)

        self.start_date = datetime.date(2018, 3, 1)
        self.initial_datetime = datetime.datetime.combine(self.start_date, self.start_time)

        self.database: sql_database_wrapper.SqlDatabaseWrapper = \
            sql_database_wrapper.SqlDatabaseWrapper.get_instance()
        self.provider = stock_data_provider.StockDataProvider.get_instance()

    def new_random_prices(self):
        current_datetime = datetime.datetime.now().replace(microsecond=0, second=0)
        data = self.database.get_first_price_all_tickers(current_datetime)
        self.randomise(data)
        data["Record_Time"] = str(current_datetime)
        self.database.insert_prices(data)

    def randomise(self, data):
        for i in range(len(data)):
            data.loc[i, "Price"] +=float(data.loc[i, "Price"]) * random.uniform(-0.09, 0.09)
        return data

    def fill_random(self):
        current_datetime=self.initial_datetime
        data = self.database.get_first_price_all_tickers(current_datetime)
        while current_datetime < datetime.datetime.now():
            self.randomise(data)
            data["Record_Time"] = str(current_datetime)
            self.database.insert_prices(data)

            current_datetime += datetime.timedelta(minutes=15)
            if current_datetime.time() > self.end_time:
                current_datetime = \
                    current_datetime.replace(hour=self.start_time.hour, minute=self.start_time.minute) + datetime.timedelta(days=1)
            if current_datetime.weekday() >= 5:
                current_datetime = current_datetime + datetime.timedelta(days=1)


if __name__ == "__main__":
    rd = RandomData.get_instance()
    rd.new_random_prices()