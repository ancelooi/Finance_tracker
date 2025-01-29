from typing import List, Dict
from pydantic import BaseModel, field_validator, Field
from datetime import datetime

#Response Models 
class UserRequest(BaseModel):
    username: str
    email: str
    password: str

#update username 
class UpdateUsernameRequest(BaseModel):
    old_username: str
    new_username: str 

#update password
class UpdateUserPassword(BaseModel):
    old_password: str 
    new_password: str


#Request Models 
class UserResponse(BaseModel):
    username: str
    email: str

class RegisterUserResponse(UserResponse): #register response 
    created_at: datetime 

class UpdatedUserResponse(BaseModel): #update response 
    updated_at: datetime 

#delete operation 
class DeleteUserResponsse(BaseModel):
    username: str 
    message: str  

# Expenses Request Models
class ExpenseRequest(BaseModel):
    username: str 
    description: str
    amount: float 
    category: str
    date: str
    @field_validator("date")
    @classmethod
    def parse_date(cls, value) -> str: 
        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%B %d, %Y"]
        for format in date_formats:
            try: 
                return datetime.strptime(value, format) #converts to ISO8601 format
            except ValueError: 
                continue 
        raise ValueError(
            f"Invalid date format: {value}. Please use one of the following formats: "
            f"YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, or 'Month DD, YYYY'."
        )


class ExpenseResponse(BaseModel):
    message: str


class CategoryItem(BaseModel):
    type: str = Field(..., pattern="^(Liability|Spending)$", description="Type must be 'Liability' or 'Spending'")
    subcategories: List[str] = Field(..., description="List of subcategories")

class AddCategoriesRequest(BaseModel):
    username: str
    new_cat: Dict[str, CategoryItem]

    @field_validator("new_cat")
    @classmethod
    def validate_new_cat(cls, value):
        if not value:
            raise ValueError("new_cat cannot be empty.")
        return value



class AssetRequest(BaseModel):
    username: str 
    name: str
    value: float 

