from fastapi import FastAPI
from app.routers import users, expenses 


app = FastAPI()

from pymongo import MongoClient
uri = "mongodb+srv://admin:dNg8cWoUftRGufPk@financetracker.ub98l.mongodb.net/?retryWrites=true&w=majority&appName=Financetracker"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

#Include Routers 
app.include_router(users.router)
app.include_router(expenses.router)


@app.get('/')
def read_root():
    return {"message": "Welcome to the Finance Tracker API"}
