from pymongo import MongoClient
uri = "mongodb+srv://admin:dNg8cWoUftRGufPk@financetracker.ub98l.mongodb.net/?retryWrites=true&w=majority&appName=Financetracker"
# Create a new client and connect to the server
client = MongoClient(uri)
database = client.finance_tracker

# Collections
users_collection = database.get_collection("users")
expenses_collection = database.get_collection("expenses")


