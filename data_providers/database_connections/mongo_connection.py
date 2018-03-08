import base.singleton as sn
import config
import urllib.parse
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.db_name = 'cs261'
        username = urllib.parse.quote_plus('root')
        password = urllib.parse.quote_plus('root')

        self.client = pymongo.MongoClient('mongodb://{}'.format(config.mongodb_host))
        self.db = self.client[self.db_name]

    def find(self, dictionary):
        self.db.posts.find_one(dictionary)

    def count(self, dictionary):
        self.db.posts.find(dictionary).count()

    def insert_one(self, data, collection):
        self.db[collection].insert_one(data)
