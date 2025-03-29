
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from neo4j import GraphDatabase

def connect_mongo():

    uri = "mongodb+srv://nyahnfetgno:Ae7U2pTws@cluster0.olivw.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
     print(e)

    return client["entertainment"]  # ta base s'appelle bien entertainment 

def connect_neo4j():
    uri = "neo4j+s://c6085e74.databases.neo4j.io"
    user = "neo4j"
    password = "erOdeAHpZ7I0FokISY646HiHhabq_Ot8EJUW07nYTHA"
    
    driver = GraphDatabase.driver(uri, auth=(user, password))


    try:
        with driver.session() as session:
            session.run("RETURN 1")
        print("✅ Connecté à Neo4j avec succès.")
    except Exception as e:
        print("❌ Erreur de connexion Neo4j :", e)

    return driver