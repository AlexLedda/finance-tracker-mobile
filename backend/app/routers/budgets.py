from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from ..models.budget import Budget, BudgetCreate
from ..core.database import db
from ..core.security import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("", response_model=Budget)
async def create_budget(budget: BudgetCreate, user_id: str = Depends(get_current_user)):
    # Check if budget exists for category
    existing = await db.db.budgets.find_one({"user_id": user_id, "category": budget.category})
    if existing:
        raise HTTPException(status_code=400, detail="Budget already exists for this category")
    
    budget_dict = budget.model_dump()
    budget_dict["user_id"] = user_id
    budget_dict["spent"] = 0
    budget_dict["created_at"] = datetime.now(timezone.utc)
    
    result = await db.db.budgets.insert_one(budget_dict)
    budget_dict["id"] = str(result.inserted_id)
    return Budget(**budget_dict)

@router.get("", response_model=List[Budget])
async def get_budgets(user_id: str = Depends(get_current_user)):
    budgets = await db.db.budgets.find({"user_id": user_id}).to_list(1000)
    return [Budget(id=str(b["_id"]), **{k: v for k, v in b.items() if k != "_id"}) for b in budgets]

@router.put("/{budget_id}", response_model=Budget)
async def update_budget(budget_id: str, budget: BudgetCreate, user_id: str = Depends(get_current_user)):
    try:
        obj_id = ObjectId(budget_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    update_dict = budget.model_dump()
    result = await db.db.budgets.update_one(
        {"_id": obj_id, "user_id": user_id},
        {"$set": update_dict}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    updated = await db.db.budgets.find_one({"_id": obj_id})
    return Budget(id=str(updated["_id"]), **{k: v for k, v in updated.items() if k != "_id"})

@router.delete("/{budget_id}")
async def delete_budget(budget_id: str, user_id: str = Depends(get_current_user)):
    try:
        obj_id = ObjectId(budget_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.db.budgets.delete_one({"_id": obj_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Budget not found")
    return {"message": "Budget deleted"}
