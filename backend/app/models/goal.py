from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Goal(BaseModel):
    id: Optional[str] = None
    user_id: str
    name: str
    target_amount: float
    current_amount: float = 0
    deadline: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now().astimezone())

class GoalCreate(BaseModel):
    name: str
    target_amount: float
    deadline: datetime
