from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from ..models.transaction import Transaction, TransactionCreate
from ..core.database import db
from ..core.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, user_id: str = Depends(get_current_user)):
    trans_dict = transaction.model_dump()
    trans_dict["user_id"] = user_id
    trans_dict["created_at"] = datetime.now(timezone.utc)
    
    result = await db.db.transactions.insert_one(trans_dict)
    
    # Update budget if expense
    if transaction.type == "expense":
        await db.db.budgets.update_one(
            {"user_id": user_id, "category": transaction.category},
            {"$inc": {"spent": transaction.amount}}
        )
    
    trans_dict["id"] = str(result.inserted_id)
    return Transaction(**trans_dict)

@router.get("", response_model=List[Transaction])
async def get_transactions(user_id: str = Depends(get_current_user)):
    transactions = await db.db.transactions.find({"user_id": user_id}).sort("date", -1).to_list(1000)
    return [Transaction(id=str(t["_id"]), **{k: v for k, v in t.items() if k != "_id"}) for t in transactions]

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str, user_id: str = Depends(get_current_user)):
    try:
        obj_id = ObjectId(transaction_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.db.transactions.delete_one({"_id": obj_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}
