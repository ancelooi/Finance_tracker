from fastapi import APIRouter, HTTPException
from app.database import assets_collection, expenses_collection
from app.schemas import AssetRequest

router = APIRouter(prefix="/networth", tags=["Net worth"]) #ensures that fastAPI routes

@router.post("/assets")
async def add_assets(asset: AssetRequest): 
    data = asset.model_dump()
    assets_collection.insert_one(data)
    return {"message": f"Asset '{asset.name}' added successfully"}


# #update assets 
# @router.put("/assets")

#calculate total net worthh
@router.get("/{username}")
async def totalnetworth(username: str):
    assets = assets_collection.find({"username":username}) #get all assets 
    liab = expenses_collection.find({"username":username}) #get all liabilities
    if not assets: 
        raise HTTPException(status_code=404, detail=f"{username} not found")
    elif not liab: 
        raise HTTPException(status_code=404, detail=f"{username} not found")
    else:
        # total_assets = 0 
        # for doc in assets: 
        #     total_assets += doc["value"]
        # total_assets = []
        total_assets = sum(doc["value"] for doc in assets)
        total_liab = 0 
        for doc in liab: 
            if doc["category_type"] == "Liability": 
                total_liab += doc["amount"]
        return f"Total networth of {username}: {total_assets-total_liab}"