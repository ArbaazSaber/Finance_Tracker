from pydantic import BaseModel, confloat
from datetime import datetime
from typing import Optional, Annotated

class CategoryTarget(BaseModel):
    target_id: int
    percentage: Annotated[float, confloat(ge=0, le=100)]
    start_date: Optional[datetime] = None
    category_id: int
    user_id: int