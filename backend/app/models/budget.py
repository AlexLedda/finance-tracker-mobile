from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Budget(BaseModel):
    id: Optional[str] = None
    user_id: str
    category: str
    limit: float
    spent: float = 0
    period: str  # monthly, weekly
    created_at: datetime = Field(default_factory=lambda: datetime.now().astimezone())

class BudgetCreate(BaseModel):
    category: str
    limit: float
    period: str
