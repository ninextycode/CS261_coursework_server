import sys, os.path
sys.path.append(os.path.abspath('../'))
from data_wrappers.StockDataProvider import StockDataProvider
from data_wrappers.SqlDatabaseConnection import SqlDatabaseConnection
import pandas as pd
import time


conn = SqlDatabaseConnection()
provider = StockDataProvider()

df = provider.get_all_stocks_data()
df1 = df[['code','name','current']]
data = list(df1.itertuples(index=False, name=None))
sql = "INSERT INTO Company VALUES (%s, %s, %s, NULL)"
conn.execute_many(sql,data)
