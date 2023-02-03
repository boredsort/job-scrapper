import os
import pymongo



class MongoClient():

    def __init__(self, url):
        self._connection = pymongo.MongoClient(url)
        self._current_db = None

    def use_db(self, db_name: str):
        self._current_db = self._connection[db_name]
        return self._current_db




