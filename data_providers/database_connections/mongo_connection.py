import base.singleton as sn
import pymongo


class MongoConnection(sn.Singleton):
    def __init__(self):
        self.client = pymongo.MongoClient()

    def get_from_db(self, name):
        db = self.client[name]

"""
        client = MongoClient()
        db = client.companyData
        collection = db.company
        posts = db.posts
        posts.find_one()
        print(collection.find_one())
        pprint.pprint(posts.find_one())
"""
