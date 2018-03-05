import base.singleton as sn
import data_providers.data_wrappers.json_database_connection as jdc


class MyData(sn.Singleton):
    def __init__(self):
        self.json_connection: jdc.JsonDatabaseConnection = jdc.JsonDatabaseConnection.get_instance()

    def add_request(self, request_data):
        self.json_connection.insert_one(request_data, collection="requests")
