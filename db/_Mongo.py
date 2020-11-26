from db._Model import *
from pymongo import MongoClient

class Mongo():
    """
    Classe che si occupa delle interazioni load/store con il db mongo
    """
    def __init__(self, db_name):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.models = Model()

    def store_tweet(self, topic, analysis):
        tweet_doc = self.models.tweet_model(topic, analysis)
        self.store(topic, tweet_doc)

    def store(self, collection, data):
        self.db[collection].insert(data)
        return True
