from fastapi import APIRouter, HTTPException
from app.database import assets_collection
from app.schemas import AssetRequest

router = APIRouter(prefix="/networth", tags=["Net worth"]) #ensures that fastAPI routes

@router.post("/assets")
async def add_assets(asset: AssetRequest): 
    data = asset.model_dump()
    assets_collection.insert_one(data)
    return {"message": f"Asset '{asset.name}' added successfully"}


# #update assets 
# @router.put("/assets")

