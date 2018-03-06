import data_providers.data_wrappers.sql_database_wrapper as sql_db
import pandas as pd


wrapper = sql_db.SqlDatabaseWrapper.get_instance()
dataframe = pd.read_csv('ftse.csv')

sectors = set(dataframe['Sector'])

for sector in sectors:
    wrapper.insert_new_sector(sector)

for ind, row in dataframe.iterrows():
    wrapper.insert_new_company(row['Ticker'], row['Company'], row['Sector'])