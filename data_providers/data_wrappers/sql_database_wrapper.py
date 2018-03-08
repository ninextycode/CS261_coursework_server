import base.singleton as sn
import data_providers.database_connections.my_sql_connection as my_sql

import datetime
import pandas as pd


class SqlDatabaseWrapper(sn.Singleton):
    def get_prices(self, tickers, many=True, time_start=None,
                   time_end=None):
        if time_end is None:
            time_end = datetime.datetime.now() \
                         + datetime.timedelta(days=1)
        if time_start is None:
            time_start = datetime.datetime(1900, 1, 1, 0, 0, 0, 0)

        query = 'SELECT Record_Time, Price, Company_code ' \
                'FROM Historical_Prices INNER JOIN Companies ' \
                'ON Companies.Company_ID = Historical_Prices.Company_ID ' \
                'WHERE %s <= Record_Time AND Record_Time <= %s ' \
                'AND Company_code IN %s' \
                'ORDER BY Record_Time DESC'
        data = self.conn.query(query,
                               [
                                   time_start, time_end, tuple(tickers)
                               ],
                               many=many)
        dataframe = pd.DataFrame([list(r) for r in data],
                                 columns=['Record_Time', 'Price', 'Company_code'])
        return dataframe

    def insert_prices(self, dataframe):
        query = 'INSERT IGNORE INTO Historical_Prices ' \
                '(Company_ID, Record_Time, Price) ' \
                'VALUES (' \
                    '(SELECT Company_ID FROM Companies WHERE Company_code=%s), ' \
                    '(%s), (%s) ' \
                ')'
        df1 = dataframe[['code', 'time', 'price']]
        data = list(df1.itertuples(index=False, name=None))
        self.conn.execute(query, data)

    def insert_new_company(self, code, name, sector):
        query = 'INSERT IGNORE INTO Companies (Company_code, Company_name, Sector_ID)' \
                'VALUES (' \
                    '(%s), ' \
                    '(%s), ' \
                    '(SELECT Sector_ID FROM Sectors WHERE Sector_Name=%s))'

        self.conn.execute(query, (code, name, sector))

    def insert_new_sector(self, sector):
        query = 'INSERT IGNORE INTO Sectors (Sector_Name)' \
                'VALUES (%s) '

        self.conn.execute(query, (sector))

    def __init__(self):
        self.conn = my_sql.MySqlConnection()

    def close(self):
        self.conn.close()

    def get_first_price_one_ticker(self, one_ticker, time):
        query = 'SELECT Record_Time, Price, Company_code ' \
                'FROM Historical_Prices  INNER JOIN Companies ' \
                'ON Companies.Company_ID = Historical_Prices.Company_ID ' \
                'WHERE Record_Time <= %s ' \
                'AND Company_code = %s ' \
                'ORDER BY Record_Time DESC LIMIT 1'

        data = self.conn.query(query, [str(time), one_ticker], many=False)

        if data is None:
            return pd.DataFrame()

        dataframe = pd.DataFrame([list(data)],
                                 columns=['Record_Time', 'Price', 'Company_code'])
        return dataframe

    def get_first_price_before(self, tickers, time):
        dataframe = pd.DataFrame()

        for ticker in tickers:
            ticker_df = self.get_first_price_one_ticker(ticker, time)
            dataframe = dataframe.append(ticker_df)

        return dataframe


if __name__ == '__main__':
    conn = SqlDatabaseWrapper()
    sql = 'SELECT * FROM COMPANY WHERE CODE = \'test\''
    print(conn.get_first_price_before(['RDSB', 'RDSA', 'AAL', 'fake'], datetime.datetime.now()))
    conn.close()


# SELECT Record_Time, Price, Company_code FROM Historical_Prices  INNER JOIN Companies ON Companies.Company_ID = Historical_Prices.Company_ID ORDER BY Record_Time DESC LIMIT 1
