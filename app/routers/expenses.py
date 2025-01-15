from fastapi import APIRouter
from app.database import expenses_collection
from app.schemas import ExpenseRequest, ExpenseResponse
from datetime import datetime
import calendar

router = APIRouter(prefix="/expenses", tags=["Expenses"]) #ensures that fastAPI routes




@router.post("/add_expenses", response_description="Add new expense")
async def add_expense(expense: ExpenseRequest) -> ExpenseResponse: 
    #convert pydantic model into a dictionary
    expense_data = expense.model_dump() 
    #insert expense into database
    expenses_collection.insert_one(expense_data)

    return ExpenseResponse(
        message="Expense added successfully"
    )

@router.get("/{username}/monthly/{year}/{month}")
async def calculate_monthly(username: str, year: int, month: int): 
    #calculate start date 
    start = datetime(year, month, 1) #1st day of the month 
    if month == 12: #if december
        end = datetime(year+1, month, 1)
    else: 
        end = datetime(year, month+1, 1)
    
    filter = {"username":username, "date":{"$gte":start, "$lte":end}}
    results = expenses_collection.find(filter)
    total = sum(doc["amount"] for doc in results)
    print(total)
    return ExpenseResponse(
        message=f"Total Expenses in {calendar.month_name[month]}: {total}" 
    )
    

@router.get("/{username}/daily/{year}/{month}/{day}")
async def calculate_daily(username: str, year: int, month: int, day: int): 
    track_day = datetime(year, month, day) #exact date to calculate expenses 
    # print(track_day)
    filter = {"username":username, "date":{"$eq": track_day}} #find all equals to date
    results = expenses_collection.find(filter)
    # print(results)

    total = sum(doc["amount"] for doc in results)
    return ExpenseResponse(
        message=f"Total Expenses on {day} {calendar.month_name[month]}: {total}" 
    )

# #yearly expenses 
@router.get("/{username}/yearly/{year}")
async def calculate_yearly(username: str, year:int):
    start = datetime(year,1,1) #1st jan 
    end = datetime(year, 12, 31) #31 dec

    filter = {"username":username, "date":{"$gte":start,"$lte":end}}
    results = expenses_collection.find(filter)
    total = sum(doc["amount"] for doc in results)

    return ExpenseResponse(
       message=f"Total Expenses in {year}: {total}" 
    )
    
    
#update expenses 



    
