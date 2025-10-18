from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryTarget(BaseModel):
    target_id: Optional[int]
    percentage: float
    start_date: datetime
    category_id: int
    user_id: int