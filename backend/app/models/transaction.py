from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[str] = None
    user_id: str
    type: str  # income or expense
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now().astimezone())

class TransactionCreate(BaseModel):
    type: str
    amount: float
    category: str
    description: Optional[str] = None
    date: datetime
