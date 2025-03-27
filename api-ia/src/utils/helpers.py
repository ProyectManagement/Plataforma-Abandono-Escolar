from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    uri = os.getenv('MONGO_URI')
    return MongoClient(uri)

def get_mongo_collection(collection_name):
    client = get_mongo_client()
    db = client[os.getenv('DB_NAME')]
    return db[collection_name]