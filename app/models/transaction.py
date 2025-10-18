from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class Transaction(BaseModel):
    transaction_id: Optional[int] = None
    transaction_time: datetime
    description: Optional[str] = None
    old_description: Optional[str] = None
    amount: Decimal
    reference_id: Optional[str] = None
    type: Optional[str] = None   # replace with Enum if desired
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    tag_id: Optional[int] = None
    category_id: Optional[int] = None
    acc_id: Optional[int] = None
    user_id: Optional[int] = None


class TransactionUpsert(BaseModel):
    transaction_time: Optional[datetime] = None
    description: Optional[str] = None
    old_description: Optional[str] = None
    amount: Optional[Decimal] = None
    reference_id: Optional[str] = None
    type: Optional[str] = None
    tag_id: Optional[int] = None
    category_id: Optional[int] = None
    acc_id: Optional[int] = None
    user_id: Optional[int] = None
