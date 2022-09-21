import os
import pymongo

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
    if not _client:
        _client = pymongo.MongoClient(url)
    return _client


def get_db():
    global _db
    if not _db:
        _db = get_client()['dbjobscraper']

    return _db

def get_collection():
    global _collection
    if not _collection:
        _collection = get_db()['scrape_data']
    return _collection

def save_scraped(job_item):
    try:
        col = get_collection()
        col.insert_one(job_item)
        return True
    except Exception as e:
        print(e)
        return False
    