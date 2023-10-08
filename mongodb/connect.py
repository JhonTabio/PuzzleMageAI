from pymongo import MongoClient

def connect(db_name, collection_name):
    # MongoDB connection settings
    uri = "mongodb+srv://matthewlabrada:Hackathong@cluster0.hvtyobg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    client = MongoClient(uri)
    db = client[str(db_name)]
    collection = db[str(collection_name)]
    return client, db, collection
