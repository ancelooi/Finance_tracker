'''CREATE READ UPDATE DELETE OPERATIONS'''
from app.database import users_collection, expenses_collection 
from app.models import User, Expense 

'''async helps to tell program that at some point in the code, it will have to wait for something else to finish somewhere'''

async def create_user(user: User): 
    new_user = await users_collection.insert_one(user.model_dump()) #to convert into json format, then store into MongoDB
    return str(new_user.inserted_id)

async def get_user_by_email(email:str):
    user = await users_collection.find_one({"email":email})
    return user 
