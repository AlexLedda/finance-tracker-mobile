from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from ..models.goal import Goal, GoalCreate
from ..core.database import db
from ..core.security import get_current_user

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("", response_model=Goal)
async def create_goal(goal: GoalCreate, user_id: str = Depends(get_current_user)):
    goal_dict = goal.model_dump()
    goal_dict["user_id"] = user_id
    goal_dict["current_amount"] = 0
    goal_dict["created_at"] = datetime.now(timezone.utc)
    
    result = await db.db.goals.insert_one(goal_dict)
    goal_dict["id"] = str(result.inserted_id)
    return Goal(**goal_dict)

@router.get("", response_model=List[Goal])
async def get_goals(user_id: str = Depends(get_current_user)):
    goals = await db.db.goals.find({"user_id": user_id}).to_list(1000)
    return [Goal(id=str(g["_id"]), **{k: v for k, v in g.items() if k != "_id"}) for g in goals]

@router.put("/{goal_id}/contribute")
async def contribute_to_goal(goal_id: str, amount: float, user_id: str = Depends(get_current_user)):
    try:
        obj_id = ObjectId(goal_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.db.goals.update_one(
        {"_id": obj_id, "user_id": user_id},
        {"$inc": {"current_amount": amount}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    updated = await db.db.goals.find_one({"_id": obj_id})
    return Goal(id=str(updated["_id"]), **{k: v for k, v in updated.items() if k != "_id"})

@router.delete("/{goal_id}")
async def delete_goal(goal_id: str, user_id: str = Depends(get_current_user)):
    try:
        obj_id = ObjectId(goal_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = await db.db.goals.delete_one({"_id": obj_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"message": "Goal deleted"}
