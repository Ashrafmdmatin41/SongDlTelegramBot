from pymongo.mongo_client import MongoClient

from MusicDllBot import MONGO_DB_URI


mongoClient = MongoClient(MONGO_DB_URI)

# collection = mongoClient["music_dll"]["ids"]