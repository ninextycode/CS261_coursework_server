from pymongo import MongoClient
import pprint

class MongoConnection:
    client = MongoClient()

    def get_from_db(name):
        db = client[name]


    client = MongoClient()
    db = client.companyData
    collection = db.company
    posts = db.posts
    posts.find_one()
    print(collection.find_one())
    pprint.pprint(posts.find_one())
