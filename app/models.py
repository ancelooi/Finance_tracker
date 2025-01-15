from typing import Optional 
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str

class Expense(BaseModel):
    user_id: str 
    category: str 
    amount: float 
    date: str 

    