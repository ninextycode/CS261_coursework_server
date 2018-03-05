import base.singleton as sn
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db_name = "cs261"
        self.db = self.client[self.db_name]

    def insert(self, dictionary):
        self.db.posts.insert_one(dictionary)

    def find(self, dictionary):
        self.db.posts.find_one(dictionary)

    def count(self, dictionary):
        self.db.posts.find(dictionary).count()
