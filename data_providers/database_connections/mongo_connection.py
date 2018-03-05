import base.singleton as sn
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_name = "cs261"
        self.db = self.client[self.db_name]

    def write(self, data):
        self.db.write(data)
