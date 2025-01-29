from pymongo import MongoClient
from app.config import settings

# Create a new client and connect to the server
client = MongoClient(settings.mongo_uri)
database = client.finance_tracker

# Collections
users_collection = database.get_collection("users")
expenses_collection = database.get_collection("expenses")
categories_collection = database.get_collection("categories")
assets_collection = database.get_collection("assets")


