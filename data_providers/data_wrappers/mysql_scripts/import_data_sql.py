import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/server',
                 '/server/data_providers/data_wrappers/mysql_scripts'])


import data_providers.data_wrappers.sql_database_wrapper as sql_db
import data_providers.data_wrappers.mysql_scripts.random_data as random_data
import pandas as pd


wrapper = sql_db.SqlDatabaseWrapper.get_instance()
dataframe = pd.read_csv('/server/data_providers/data_wrappers/mysql_scripts/ftse.csv')

sectors = set(dataframe['Sector'])

for sector in sectors:
    wrapper.insert_new_sector(sector)

for ind, row in dataframe.iterrows():
    wrapper.insert_new_company(row['Ticker'], row['Company'], row['Sector'])

random_data.RandomData.get_instance().fill_1000()
random_data.RandomData.get_instance().fill_random()