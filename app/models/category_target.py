from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional

class CategoryTargetCreate(BaseModel):
    percentage: Optional[float]
    start_date: Optional[datetime] = None
    category_id: int
    user_id: int

class CategoryTargetUpdate(BaseModel):
    percentage: Optional[float]
    start_date: Optional[datetime] = None

class CategoryTargetInDB(BaseModel):
    target_id: int
    percentage: Optional[float]
    start_date: datetime
    category_id: int
    user_id: int
