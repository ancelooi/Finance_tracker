from fastapi import APIRouter, HTTPException
from app.crud import create_user, get_user_by_email
from app.schemas import UserRequest, UserResponse, DeleteUserResponsse, RegisterUserResponse, UpdateUsernameRequest, UpdatedUserResponse 
from app.database import users_collection
import datetime

router = APIRouter(prefix="/users", tags=['Users']) #omits the need to write /users/register in routes 

#find user 
@router.get("/")
def display_users():
    cursor = users_collection.find({})
    for i in cursor: 
        print(i)
    return 

    

# Register user 
@router.post("/register", response_model=RegisterUserResponse)
async def register(user: UserRequest) -> RegisterUserResponse: #returns a user response object
    existing = users_collection.find_one({"username":user.username}) #query to find username 
    if existing: 
        raise HTTPException(status_code=400, detail="Username taken")
    user_data = user.model_dump() #converts it into a dictionary
    user_data['created_at'] = datetime.datetime.now()
    users_collection.insert_one(user_data)
    return RegisterUserResponse(
        username=user.username,
        email=user.username,
        created_at = user_data['created_at']
        )

#Delete user #to pass e.g. http://127.0.0.1:8000/users/john123
@router.post("/{username}",response_model=DeleteUserResponsse)
async def delete_user(username:str) -> DeleteUserResponsse:
    existing = users_collection.find_one({"username":username})
    if not existing: 
        raise HTTPException(status_code=400, detail="username not found")

    users_collection.delete_one({"username":username})
    return DeleteUserResponsse(
        username=username,
        message="User successfully deleted. ")

#Update username 
@router.put('/{username}')
async def update_username(username: str, new_data: UpdateUsernameRequest):
    existing = users_collection.find_one({"username": username})
    if not existing: 
        raise HTTPException(status_code=400, detail="username not found")
    filter = {"username": username}
    newvalues = {"$set": {"username":new_data.new_username}}
    users_collection.update_one(filter, newvalues)
    return UpdatedUserResponse(
        username= new_data.new_username,
        updated_at=datetime.datetime.now()
    )



    



