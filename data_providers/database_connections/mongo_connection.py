import base.singleton as sn
import config

import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient(host=config.mongodb_host)
        self.db_name = 'cs261'
        self.db = self.client[self.db_name]

    def find(self, dictionary):
        self.db.posts.find_one(dictionary)

    def count(self, dictionary):
        self.db.posts.find(dictionary).count()

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)
