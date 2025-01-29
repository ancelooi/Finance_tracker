from fastapi import APIRouter, HTTPException
from app.schemas import AddCategoriesRequest
from typing import Dict, List
from app.database import categories_collection

# Initialize router
router = APIRouter(prefix="/categories", tags=["Categories"])


# Add categories endpoint
@router.post("/")
async def add_categories(request: AddCategoriesRequest):
    username = request.username
    new_cat = request.new_cat

    # Convert Pydantic models to plain dictionaries
    new_cat_dict = {key: value.dict() for key, value in new_cat.items()}

    # Check if the user already has categories
    existing = categories_collection.find_one({"username": username})
    if existing:
        # Merge existing categories with new categories
        updated_categories = {**existing["categories"], **new_cat_dict}
        categories_collection.update_one(
            {"username": username},
            {"$set": {"categories": updated_categories}}
        )
    else:
        # Create a new document for the user
        categories_collection.insert_one({
            "username": username,
            "categories": new_cat_dict
        })

    return {"message": "Categories added successfully"}


# Retrieve categories endpoint
@router.get("/{username}")
async def get_user_categories(username: str):
    user_categories = categories_collection.find_one({"username": username})
    if not user_categories:
        raise HTTPException(status_code=404, detail="No categories found for this user.")
    return {"categories": user_categories["categories"]}
