import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
from data_providers.data_wrappers.StockDataProvider import StockDataProvider
from data_providers.data_wrappers.SqlDatabaseConnection import SqlDatabaseConnection
import pandas as pd
import time


class StockDatabaseUpdater:
    provider = StockDataProvider()
    conn = None
    currentDf = None
    isUpdate = True

    def __update():
        StockDatabaseUpdater.currentDf = StockDatabaseUpdater.provider.get_all_stocks_data()
        df1 = StockDatabaseUpdater.currentDf[['code','time','price']]
        data = list(df1.itertuples(index=False, name=None))
        sql = "INSERT INTO Historical_Price VALUES (%s, %s, %s)"
        StockDatabaseUpdater.conn.execute_many(sql,data)

    def update():
        StockDatabaseUpdater.conn = SqlDatabaseConnection()
        while (StockDatabaseUpdater.isUpdate):
            StockDatabaseUpdater.__update()
            time.sleep(300)
        conn.close()

if __name__ == '__main__':
    """
    conn = SqlDatabaseConnection()
    provider = StockDataProvider()

    df = provider.get_all_stocks_data()
    df1 = df[['code','name','current']]
    data = list(df1.itertuples(index=False, name=None))
    sql = "INSERT INTO Company VALUES (%s, %s, %s, NULL)"
    conn.execute_many(sql,data)
    """
    StockDatabaseUpdater.update()
