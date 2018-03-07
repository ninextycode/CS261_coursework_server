import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/server',
                 '/server/data_providers/data_wrappers/mysql_scripts'])



import data_providers.data_wrappers.stock_data_provider as stock_data_provider
import data_providers.data_wrappers.sql_database_wrapper as sql_database_wrapper

import datetime

import numpy as np
import pandas as pd

import random
# 7:50 a.m. with an opening auction and ends at 4:35 p.m
start_time = datetime.time(7, 50)
end_time = datetime.time(16, 35)

start_date = datetime.date(2017, 10, 1)
current_datetime = datetime.datetime.combine(start_date, start_time)

database: sql_database_wrapper.SqlDatabaseWrapper = sql_database_wrapper.SqlDatabaseWrapper.get_instance()
provider = stock_data_provider.StockDataProvider.get_instance()

data = provider.get_all_stocks_data()
data["price"] = data["price"].convert_objects(convert_numeric=True)
while current_datetime <= datetime.datetime.now():
    # print(data.loc[2, "price"])
    data["time"] = str(current_datetime)
    database.insert_prices(data)

    for i in range(len(data)):
        data.loc[i, "price"] += float(data.loc[i, "price"]) * random.uniform(-0.02, 0.02)

    print(current_datetime)
    current_datetime += datetime.timedelta(minutes=15)
    if current_datetime.time() > end_time:
        current_datetime = \
            current_datetime.replace(hour=start_time.hour, minute=start_time.minute) + datetime.timedelta(days=1)
    if current_datetime.weekday() >= 5:
        current_datetime = current_datetime + datetime.timedelta(days=1)