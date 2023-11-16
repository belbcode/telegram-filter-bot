from pymongo import MongoClient
from mongoengine import connect
import os, dotenv

dotenv.load_dotenv()

def connect_to_db():
    connection_string = os.getenv("MONGODB_CONNECTION_STRING", None)
    if not connection_string:
        raise ValueError("Connection string not provided in .env")
    connect(host=connection_string)