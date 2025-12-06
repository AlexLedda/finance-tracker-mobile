from pydantic import BaseModel
from typing import Optional

class AdviceRequest(BaseModel):
    context: Optional[str] = None
