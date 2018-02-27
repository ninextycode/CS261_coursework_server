import base.singleton as sn
import data_providers.database_connections.mongo_connection as mongo
import datetime


class JsonDatabaseConnection(sn.Singleton):
    def __init__(self):
        self.database_connection = mongo.MongoConnection.get_instance()

    def write(self, data):
        data["time"] = datetime.datetime
        self.database_connection.w