import base.singleton as sn


import data_providers.data_wrappers.stock_data_provider as stock_data
import data_providers.data_wrappers.sql_database_connection as sql_db
import pandas as pd
import time


class StockDatabaseUpdater(sn.Singleton):
    def __init__(self):
        self.provider = stock_data.StockDataProvider.get_instance()
        self.conn = sql_db.SqlDatabaseConnection.get_instance()
        self.currentDf = None
        self.isUpdate = True

    def __update(self):
        StockDatabaseUpdater.currentDf = self.provider.get_all_stocks_data()
        df1 = StockDatabaseUpdater.currentDf[["code","time","price"]]
        data = list(df1.itertuples(index=False, name=None))
        sql = "INSERT INTO Historical_Price VALUES (%s, %s, %s)"
        self.conn.execute_many(sql,data)

    def update(self):
        StockDatabaseUpdater.conn = sql_db.SqlDatabaseConnection()
        while self.isUpdate:
            self.__update()
            time.sleep(300)
        self.conn.close()


if __name__ == "__main__":
    """
    conn = SqlDatabaseConnection()
    provider = StockDataProvider()

    df = provider.get_all_stocks_data()
    df1 = df[["code","name","current"]]
    data = list(df1.itertuples(index=False, name=None))
    sql = "INSERT INTO Company VALUES (%s, %s, %s, NULL)"
    conn.execute_many(sql,data)
    """
    StockDatabaseUpdater.get_instance().update()
