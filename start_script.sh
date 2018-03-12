mysql -h mysql -u root -proot cs261 < /server/data_providers/data_wrappers/mysql_scripts/schema.sql
python3 /server/data_providers/data_wrappers/mysql_scripts/import_data_sql.py
python3 /server/business_logic/notifications/advice_database_filler.py
python3 main.py