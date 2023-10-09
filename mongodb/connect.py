from pymongo import MongoClient

def connect(db_name, collection_name):
    # MongoDB connection settings
    uri = "ENTER_ATLAS_CONNECTION_STRING_HERE"
    client = MongoClient(uri)
    db = client[str(db_name)]
    collection = db[str(collection_name)]
    return client, db, collection
