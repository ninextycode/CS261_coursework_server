import base.singleton as sn
import data_providers.data_wrappers.json_database_connection as jdc


class MyData(sn.Singleton):
    def __init__(self):
        self.json_connection: jdc.JsonDatabaseConnection = jdc.JsonDatabaseConnection.get_instance()

    def add_request(self, request_data):
        copy = {**request_data}
        self.json_connection.insert_one(copy, collection="requests")

    def count_request_with_this_keyword(self, keyword):
        self.json_connection.count({})

if __name__ == "__main__":
    conn = MyData.get_instance()
    conn.add_request({"test": 0})
