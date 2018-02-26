import data_providers.data_wrappers.stock_data_provider as stock_data
import data_providers.data_wrappers.sql_database_connection as sql_db


conn = sql_db.SqlDatabaseConnection.get_instance()
provider = stock_data.StockDataProvider.get_instance()

df = provider.get_all_stocks_data()
df1 = df[["code", "name", "current"]]
data = list(df1.itertuples(index=False, name=None))
sql = "INSERT INTO Company VALUES (%s, %s, %s, NULL)"
conn.execute_many(sql,data)
