import base.singleton as sn
import config
import urllib.parse
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.db_name = 'cs261'
        self.client = pymongo.MongoClient('mongodb://{}'.format(config.mongodb_host))
        self.db = self.client[self.db_name]

    def find(self, dictionary, collection):
        return self.db[collection].find(dictionary)

    def count(self, dictionary, collection):
        posts = self.db[collection].find(dictionary)
        return posts.count()

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)

    def update(self, key, data, collection):
        self.db[collection].update(key, data, upsert=True)