from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from app.database import assets_collection, expenses_collection, investments_collection, loans_collection, savings_collection
from app.schemas import SavingsRequest, InvestmentRequest, LoanRequest
from typing import List

router = APIRouter(prefix="/planning", tags=["Financial Planning"])

@router.post("/savings")
async def add_savings_goal(savings: SavingsRequest):
    data = savings.model_dump()
    savings_collection.insert_one(data)
    progress = (savings.amount / savings.goal) * 100
    return {
        "message": f"Savings goal added successfully",
        "progress": f"{progress:.2f}%"
    }

@router.post("/investments")
async def add_investment(investment: InvestmentRequest):
    data = investment.model_dump()
    investments_collection.insert_one(data)
    projected_value = investment.amount * (1 + investment.expected_return/100)
    return {
        "message": f"Investment added successfully",
        "projected_value": projected_value
    }

@router.post("/loans")
async def add_loan(loan: LoanRequest):
    data = loan.model_dump()
    loans_collection.insert_one(data)
    
    # Calculate total payment
    duration_months = (loan.end_date - loan.start_date).days / 30
    total_payment = loan.payment_amount * duration_months
    total_interest = total_payment - loan.principal
    
    return {
        "message": f"Loan '{loan.name}' added successfully",
        "total_interest": total_interest,
        "total_payment": total_payment
    }


#financial summary of user's assets, investments and loans 
@router.get("/{username}/financial-summary")
async def get_financial_summary(username: str):
    # Get all financial data
    assets = assets_collection.find({"username": username})
    investments = investments_collection.find({"username": username})
    loans = loans_collection.find({"username": username})
    savings = savings_collection.find({"username": username})
    
    # Calculate totals
    total_assets = sum(doc["value"] for doc in assets)
    total_investments = sum(doc["amount"] for doc in investments)
    total_loans = sum(doc["principal"] for doc in loans)
    total_savings = sum(doc["amount"] for doc in savings)
    
    net_worth = total_assets + total_investments - total_loans
    
    return {
        "net_worth": net_worth,
        "total_assets": total_assets,
        "total_investments": total_investments,
        "total_loans": total_loans,
        "total_savings": total_savings
    }