import os
import pymongo
import traceback

from dotenv import load_dotenv

load_dotenv()

url = os.getenv('mongo_url')

# mycol = mydb["scrape_data"]

# mydict = { "name": "John", "address": "Highway 37" }

# db = mydb.test

# x = mycol.insert_one(mydict)

_client = None
_db = None
_collection = None

def get_client():
    global _client
    if _client is None:
        _client = pymongo.MongoClient(url)
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()['dbjobscraper']

    return _db

def get_collection():
    global _collection
    if _collection is None:
        _collection = get_db()['scrape_data']
    return _collection

def save_scraped(job_item):
    try:
        col = get_collection()
        res = col.insert_one(job_item)
        return res.inserted_id.__str__(), None
    except Exception as e:
        print(e)
        return None, traceback.format_exc()
    