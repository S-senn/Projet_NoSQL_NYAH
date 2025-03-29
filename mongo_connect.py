# mongo_connect.py
from pymongo import MongoClient

def get_collection():
    uri = "mongodb+srv://nyahnfetgno:Ae7U2pTws@cluster0.olivw.mongodb.net/?appName=Cluster0"
    client = MongoClient(uri)
    return client["entertainment"]["films"]
