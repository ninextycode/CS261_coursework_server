import base.singleton as sn

import datetime
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_name = "cs261"
        self.db = self.client[self.db_name]
        self.db.add_son_manipulator()

    def find(self, name):
        db = self.client[name]

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)
