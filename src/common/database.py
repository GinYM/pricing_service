import pymongo
import src.website_config as config


class Database(object):
    URI = config.MONGODB_URI
    #URI = os.environ.get('MONGODB_URI').replace('\"',"")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['full_stack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, criteria, objNew):
        Database.DATABASE[collection].update(criteria, {"$set": objNew}, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def count(collection, query):
        return Database.DATABASE[collection].count(query)
