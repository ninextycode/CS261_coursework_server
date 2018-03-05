import base.singleton as sn
import data_providers.database_connections.mongo_connection as mongo
import datetime


class JsonDatabaseConnection(sn.Singleton):
    def __init__(self):
        self.database_connection = mongo.MongoConnection.get_instance()
        self.database_connection: mongo.MongoConnection = mongo.MongoConnection.get_instance()

    def insert_one(self, data, collection="default"):
        data["time"] = datetime.datetime.now()
        self.database_connection.insert_one(data, collection)


if __name__ == "__main__":
    conn = JsonDatabaseConnection.get_instance()
    conn.insert_one({"test": 0})
