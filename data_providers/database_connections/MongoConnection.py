from pymongo import MongoClient
import pprint

client = MongoClient()
db = client.companyData
collection = db.company
posts = db.posts
posts.find_one()
print(collection.find_one())
pprint.pprint(posts.find_one())
