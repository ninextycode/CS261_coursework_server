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
        self.db[collection].posts.find(dictionary)

    def count(self, dictionary, collection):
        posts = self.db[collection].find(dictionary)
        for post in posts:
            print(post)
        return posts.count()

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)
