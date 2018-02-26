from pymongo import MongoClient
import pprint

class MongoConnection:
    def __init__(self):
        self.client = MongoClient()

    def get_from_db(name):
        db = MongoConnection.client[name]


        client = MongoClient()
        db = client.companyData
        collection = db.company
        posts = db.posts
        posts.find_one()
        print(collection.find_one())
        pprint.pprint(posts.find_one())
