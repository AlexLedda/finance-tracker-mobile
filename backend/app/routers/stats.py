from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime, timedelta
from ..core.database import db
from ..core.security import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("")
async def get_stats(user_id: str = Depends(get_current_user)):
    # Get all transactions
    transactions = await db.db.transactions.find({"user_id": user_id}).to_list(1000)
    
    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expenses
    
    # Category breakdown
    category_expenses = {}
    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            category_expenses[category] = category_expenses.get(category, 0) + t["amount"]
    
    # Recent transactions (last 30 days)
    # Note: ensure dates are comparable (offset-naive vs aware). 
    # Stored dates might be naive if they came from utcnow() in the past.
    # New ones are aware. We'll handle this loosely or ensure naive comparison.
    thirty_days_ago = datetime.utcnow() - timedelta(days=30) 
    # Ideally use datetime.now(timezone.utc) but if DB has mixed, let's stick to safe comparison or conversion
    
    # Let's try to be consistent with what was there, but maybe improve if possible.
    # The original code used datetime.utcnow().
    
    recent_transactions = []
    for t in transactions:
        t_date = t["date"]
        # If t_date is string, parse it? PyMongo usually returns datetime objects.
        # If t_date is offset-aware, we need offset-aware 30 days ago.
        if t_date.tzinfo is not None:
             thirty_days_ago_aware = datetime.now(t_date.tzinfo) - timedelta(days=30)
             if t_date >= thirty_days_ago_aware:
                 recent_transactions.append(t)
        else:
             # Fallback for old data
             if t_date >= thirty_days_ago:
                 recent_transactions.append(t)

    recent_income = sum(t["amount"] for t in recent_transactions if t["type"] == "income")
    recent_expenses = sum(t["amount"] for t in recent_transactions if t["type"] == "expense")
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "category_expenses": category_expenses,
        "recent_income": recent_income,
        "recent_expenses": recent_expenses,
        "transaction_count": len(transactions)
    }
