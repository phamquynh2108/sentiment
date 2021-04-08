from pymongo import MongoClient
import time, sys
from bson.objectid import ObjectId
from loguru import logger

class MongoDatabase:
    def __init__(self, client):

        self.client = MongoClient()
        self.db = self.client[client]

    def read_collection(self, collection):
        try:
            return self.db[collection].find({}, no_cursor_timeout=True)
        except Exception as e:
            logger.error("[{}] : {}".format(sys._getframe().f_code.co_name, e))
            exit(1)

    def insert_one_to_collection(self, collection, doc):
        try:
            self.db[collection].insert_one(doc)
        except Exception as e:
            logger.error("[{}] : {}".format(sys._getframe().f_code.co_name, e))
            exit(1)

    def update_collection(self, collection, doc):
        try:
            self.db[collection].update({'_id' : ObjectId(doc['_id'])}, doc, upsert = False)
        except Exception as e:
            logger.error("[{}] : {}".format(sys._getframe().f_code.co_name, e))
            exit(1)
